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


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()  # Retrieve all Sale objects
    serializer_class = SaleSerializer  # Use the SaleSerializer

    @action(methods=['get'], detail=False)
    def monthly_sales_comparison(self, request):
        """
        Returns the total ladies-night sales and event sales for each month,
        e.g. for a bar chart in the frontend.
        """
        # 1) Group sales by month (based on the 'date' field).
        # 2) Annotate with sum of ladies-night sales and sum of event sales.
        
        sales_data = (
            Sale.objects
            .annotate(month=ExtractMonth('date'))
            .values('month')
            .annotate(
                # For Ladies Night: sum arcade_sales where ladies_night=True
                ladies_night_sales=Sum(
                    'arcade_sales',
                    filter=Q(ladies_night=True)
                ),
                # For Events: sum event_amount where Event is not null/blank
                # (Adjust if you want to include more fields, e.g. cafe_sales, etc.)
                event_sales=Sum(
                    'event_amount',
                    filter=Q(Event__isnull=False)
                )
            )
            .order_by('month')
        )

        # Map month numbers to month names
        month_names = {
            1: 'January', 2: 'February', 3: 'March',     4: 'April',
            5: 'May',     6: 'June',     7: 'July',      8: 'August',
            9: 'September',10: 'October',11: 'November',12: 'December'
        }
        
        # Prepare data for the Chart.js-style response
        labels = [month_names.get(item['month'], str(item['month'])) for item in sales_data]

        ladies_night_data = [item['ladies_night_sales'] or 0 for item in sales_data]
        event_data        = [item['event_sales']        or 0 for item in sales_data]
        
        response_data = {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Ladies Night',
                    'data': ladies_night_data,
                    # No need to hardcode backgroundColor / borderColor
                    # unless you want to. Let the frontend handle styling.
                },
                {
                    'label': 'Events',
                    'data': event_data,
                },
            ]
        }
        return Response(response_data)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()  # Retrieve all Expense objects
    serializer_class = ExpenseSerializer  # Use the ExpenseSerializer