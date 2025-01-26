from rest_framework import viewsets
from .models import Sale, Expense
from .serializers import SaleSerializer, ExpenseSerializer
from datetime import datetime, timedelta
from rest_framework.decorators import action
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.functions import ExtractMonth  # Import ExtractMonth

from django.db.models import F, Sum, ExpressionWrapper, DecimalField, Q  # Import Q and other necessary modules
from django.db.models.functions import ExtractMonth  # Import ExtractMonth
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Sale  # Import your Sale model
from datetime import date, timedelta
from django.db.models.functions import TruncMonth
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import pandas as pd
from django.db.models import Case, When, Value
from Liabilities.models import Liability
from django.http import HttpResponse
from django.utils.timezone import now


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()  # Retrieve all Sale objects
    serializer_class = SaleSerializer  # Use the SaleSerializer
    parser_classes = [MultiPartParser]  # Enable file uploads via API
    

    def list(self, request, *args, **kwargs):
        # Call the default list method to get serialized data
        response = super().list(request, *args, **kwargs)

        currentmonth = date.today()
        current_month = now().month

        # Calculate totals for the required fields
        totals = Sale.objects.filter(date__month=current_month).aggregate(
            total_arcade_sales=Sum('arcade_sales'),
            total_event_sales=Sum('event_amount', filter=Q(Event__isnull=False)),
            total_cafe_expenses=Sum('cafe_expenses'),
            total_other_expenses=Sum('other_expenses'),
            total_event_amount=Sum('event_amount')
        )

        # Construct the final response
        response_data = {
            "totals": {
                "arcade_sales": totals['total_arcade_sales'] or 0,
                "event_sales": totals['total_event_sales'] or 0,
                "cafe_expenses": totals['total_cafe_expenses'] or 0,
                "other_expenses": totals['total_other_expenses'] or 0,
                "event_amount": totals['total_event_amount'] or 0,
            },
            "data": response.data  # Original serialized data
        }

        return Response(response_data)

    @action(detail=False, methods=['get'], url_path='download')
    def download(self, request):
        """
        Generate and download an Excel file with filtered sales data.
        """
        # Fetch filtered data based on start and end dates
        sales = self.get_queryset()

        # Convert the data to a pandas DataFrame
        data = sales.values(
            'date',
            'Event',
            'event_amount',
            'arcade_sales',
            'cafe_sales',
            'cafe_expenses',
            'other_expenses'
            
        )
        df = pd.DataFrame(data)

        # Format the date column
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%d-%b-%Y')

        # Create an Excel file in memory
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="sales_data.xlsx"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sales')

        return response

    @action(methods=['get'], detail=False)
    def monthly_sales_comparison(self, request):
        """
        Returns the total "Ladies Night" sales and event sales for each month,
        e.g., for a bar chart in the frontend.
        """
        # Group sales by month (based on the 'date' field)
        sales_data = (
            Sale.objects
            .annotate(month=ExtractMonth('date'))
            .values('month')
            .annotate(
                # For Ladies Night: sum arcade_sales where Event="Ladies Night"
                ladies_night_sales=Sum(
                    'arcade_sales',
                    filter=Q(Event__iexact="Ladies Night")  # Use case-insensitive matching
                ),
                # For Events: sum event_amount where Event is not null/blank
                event_sales=Sum(
                    'event_amount',
                    filter=Q(Event__isnull=False) & ~Q(Event__iexact="Ladies Night")  # Exclude "Ladies Night" events
                )
            )
            .order_by('month')
        )

        # Map month numbers to month names
        month_names = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }

        # Prepare data for the Chart.js-style response
        labels = [month_names.get(item['month'], str(item['month'])) for item in sales_data]

        ladies_night_data = [item['ladies_night_sales'] or 0 for item in sales_data]
        event_data = [item['event_sales'] or 0 for item in sales_data]

        response_data = {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Ladies Night',
                    'data': ladies_night_data,
                },
                {
                    'label': 'Other Events',
                    'data': event_data,
                },
            ]
        }
        return Response(response_data)


    @action(methods=['get'], detail=False)
    def monthly_data(self, request):
        """
        Returns the monthly data for a specified field (e.g., cafe_sales, arcade_sales, etc.).
        """
        # Extract the field from query parameters
        field = request.query_params.get('field', 'arcade_sales')  # Default to 'arcade_sales'
        valid_fields = ['cafe_sales', 'event_amount', 'arcade_sales', 'cafe_expenses', 'other_expenses', 'total_profit']
        year = request.query_params.get('year', None)  # Get the year from query parameters
        
        if field not in valid_fields:
            return Response({'error': f'Invalid field. Choose from {valid_fields}.'}, status=400)

        # Define a custom annotation for total_profit
        annotated_data = Sale.objects.filter(date__year=year).annotate(
            month=ExtractMonth('date'),
            cafe_profit=Case(
                When(event_amount__isnull=False, then=F('cafe_sales') + F('event_amount') - F('cafe_expenses')),
                default=F('cafe_sales') - F('cafe_expenses'),
                output_field=DecimalField()
            ),
            total_profit=(
                Case(
                    When(event_amount__isnull=False, then=F('cafe_sales') + F('event_amount') - F('cafe_expenses')),
                    default=F('cafe_sales') - F('cafe_expenses'),
                    output_field=DecimalField()
                ) +
                F('arcade_sales') -
                F('other_expenses')
            )
        )

        # Aggregate the specified field by month
        data = (
            annotated_data
            .values('month')
            .annotate(total=Sum(field if field != 'total_profit' else 'total_profit'))  # Handle total_profit annotation
            .order_by('month')
        )

        # Map month numbers to names
        month_names = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }

        # Format response
        response_data = {
            'labels': [month_names.get(item['month'], str(item['month'])) for item in data],
            'data': [item['total'] or 0 for item in data],  # Handle None values
            'field': field,
        }
        return Response(response_data)

    

    @action(methods=['get'], detail=False)
    def monthly_chart_data(self, request):
        """
        Returns aggregated sales data for the current month and last month.
        """
        # Get the current date and calculate last month's date
        today = date.today()
        current_month_start = today.replace(day=1)
        three_months_ago_start = (current_month_start - timedelta(days=1)).replace(day=1)
        three_months_ago_start = (three_months_ago_start - timedelta(days=1)).replace(day=1)
        three_months_ago_start = (three_months_ago_start - timedelta(days=1)).replace(day=1)

        # Filter and aggregate data for the last three months
        sales_data = Sale.objects.filter(
            date__gte=three_months_ago_start,
            date__lt=current_month_start  # Exclude the current month
        ).annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            arcade_sales=Sum('arcade_sales'),
            cafe_sales=Sum('cafe_sales'),
            cafe_expenses=Sum('cafe_expenses'),
            other_expenses=Sum('other_expenses'),
            event_sales=Sum('event_amount')
        ).order_by('month')

        # Format response data
        response_data = {
            "labels": [item['month'].strftime('%B') for item in sales_data],
            "arcade_sales": [item['arcade_sales'] or 0 for item in sales_data],
            "cafe_sales": [item['cafe_sales'] or 0 for item in sales_data],
            "cafe_expenses": [item['cafe_expenses'] or 0 for item in sales_data],
            "other_expenses": [item['other_expenses'] or 0 for item in sales_data],
            "event_sales": [item['event_sales'] or 0 for item in sales_data],
        }

        return Response(response_data)
    

    @action(detail=False, methods=['post'], url_path='data-upload')
    def data_upload(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file was provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file into a dictionary of DataFrames
            excel_data = pd.read_excel(file, sheet_name=None, engine='openpyxl')

            # Prepare containers for validated data
            sales_data = []
            liabilities_data = []

            # # Validate and process the 'sales' sheet if it exists
            if 'sales' in excel_data:
                df = excel_data['sales']

                # Preprocess the DataFrame
                df = df.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)  # Clean strings
                df.replace({'N/A': None, 'n/a': None, '': None}, inplace=True)  # Replace placeholders
                df = df.dropna(how='all')  # Drop completely empty rows
                df = df.dropna(
                    subset=['date', 'arcade_sales', 'cafe_sales', 'event_sales', 'cafe_expenses', 'other_expenses'],
                    how='all'
                )  # Drop rows where all relevant columns are NaN
                df = df.reset_index(drop=True)  # Reset index after dropping rows

                try:
                    # Iterate through each cell to validate
                    for index, row in df.iterrows():
                        for col in ['date', 'arcade_sales', 'cafe_sales', 'event_sales', 'cafe_expenses', 'other_expenses']:
                            value = row.get(col, None)
                            if col == 'date':
                                pd.to_datetime(value, errors='raise')  # Ensure valid date
                            else:
                                # Replace invalid values like 'N/A' with NaN and test conversion
                                if isinstance(value, str) and value.strip().upper() == 'N/A':
                                    raise ValueError(f"Invalid value 'N/A' in column '{col}'")
                                pd.to_numeric(value, errors='raise')  # Ensure valid numeric

                    # Handle missing or invalid data for Sales
                    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Ensure valid dates
                    df['arcade_sales'] = pd.to_numeric(df['arcade_sales'], errors='coerce').fillna(0)
                    df['cafe_sales'] = pd.to_numeric(df['cafe_sales'], errors='coerce').fillna(0)
                    df['event_amount'] = pd.to_numeric(df['event_sales'], errors='coerce').fillna(0)
                    df['cafe_expenses'] = pd.to_numeric(df['cafe_expenses'], errors='coerce').fillna(0)
                    df['other_expenses'] = pd.to_numeric(df['other_expenses'], errors='coerce').fillna(0)
                    # Replace NaN in the 'event' column with None
                    df['event'] = df['event'].where(pd.notnull(df['event']), None)

                    # Filter out rows with invalid or missing dates
                    df = df.dropna(subset=['date'])

                    # Collect validated data for sales
                    for _, row in df.iterrows():
                        sale_date = row['date'].date()
                        # If Monday => Ladies Night (and zero event_amount), else use row['event_sales']
                        sales_data.append(Sale(
                            date=sale_date,
                            Event="Ladies Night" if sale_date.weekday() == 0 else row['event'],
                            event_amount=0 if sale_date.weekday() == 0 else row['event_sales'],
                            cafe_sales=row['cafe_sales'],
                            arcade_sales=row['arcade_sales'],
                            cafe_expenses=row['cafe_expenses'],
                            other_expenses=row['other_expenses'],
                        ))
                except Exception as e:
                    print(f"Problematic row in 'sales': {row}")  # Log the entire row for debugging
                    return Response(
                        {"error": f"Error in 'sales' sheet at row {index + 1}, column '{col}': {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Validate and process the 'liabilities' sheet if it exists
            if 'liabilities' in excel_data:
                df = excel_data['liabilities']

                try:
                    # Iterate through each cell to validate
                    for index, row in df.iterrows():
                        for col in ['date', 'amount', 'user']:
                            value = row.get(col, None)
                            if col == 'date':
                                pd.to_datetime(value, errors='raise')
                            elif col == 'amount':
                                pd.to_numeric(value, errors='raise')
                            # 'user' column is optional, so no strict validation here

                    # Handle missing or invalid data for Liabilities
                    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
                    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Ensure valid dates

                    # Filter out rows with invalid or missing dates
                    df = df.dropna(subset=['date'])

                    # Collect validated data for liabilities
                    for _, row in df.iterrows():
                        liabilities_data.append(Liability(
                            date=row['date'].date(),
                            amount=row['amount'],
                            user=row['user'] if pd.notnull(row['user']) else None,
                        ))
                except Exception as e:
                    print(f"Problematic row in 'liabilities': {row}")
                    return Response(
                        {"error": f"Error in 'liabilities' sheet at row {index + 1}, column '{col}': {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # If both sheets are valid, perform the bulk insert
            try:
                if sales_data:
                    Sale.objects.bulk_create(sales_data)
                if liabilities_data:
                    Liability.objects.bulk_create(liabilities_data)
            except Exception as e:
                return Response(
                    {"error": f"An error occurred while saving data to the database: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # If no recognized sheets exist
            if not sales_data and not liabilities_data:
                return Response({"error": "Sheet name must be either 'Sales' or 'Liabilities'."}, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {
                    "sales": f"Successfully inserted {len(sales_data)} Sales records." if sales_data else "No sales data processed.",
                    "liabilities": f"Successfully inserted {len(liabilities_data)} Liability records." if liabilities_data else "No liabilities data processed."
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred while processing the file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )







class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()  # Retrieve all Expense objects
    serializer_class = ExpenseSerializer  # Use the ExpenseSerializer




from rest_framework import viewsets
from .models import InventoryItem, Category, SubCategory
from .serializers import InventoryItemSerializer, CategorySerializer, SubCategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.select_related('category').all()
    serializer_class = SubCategorySerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.select_related('category', 'subcategory').all()
    serializer_class = InventoryItemSerializer
