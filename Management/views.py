from rest_framework import viewsets
from .models import Staff, Task, Target, Meeting,StaffProfile,Customer, CustomerVisit
from .Serializers import (
    StaffSerializer, TaskSerializer, TargetSerializer, MeetingSerializer, ArcadeQuestionSerializer,
    ArcadeFeedbackSerializer,
    CafeQuestionSerializer,
    CafeFeedbackSerializer,StaffProfileSerializer,
    CustomerSerializer,CustomerVisitSerializer
)



class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer



from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from rest_framework import viewsets
from .models import (
    ArcadeQuestion,
    ArcadeFeedback,
    CafeQuestion,
    CafeFeedback,
    Customer
)

# ------------------ Arcade ViewSets ------------------ #
class ArcadeQuestionViewSet(viewsets.ModelViewSet):
    queryset = ArcadeQuestion.objects.all()
    serializer_class = ArcadeQuestionSerializer


# class ArcadeFeedbackViewSet(viewsets.ModelViewSet):
#     queryset = ArcadeFeedback.objects.all()
#     # queryset = ArcadeFeedback.objects.select_related('customer', 'question')
#     serializer_class = ArcadeFeedbackSerializer

#     # def create(self, request, *args, **kwargs):
#     #     # Extract top-level data
#     #     customer_name = request.data.get('customer_name')
#     #     customer_email = request.data.get('customer_email', '')
#     #     customer_contact = request.data.get('customer_contact', '')
#     #     feedbacks_data = request.data.get('feedbacks', [])

#     #     # 1) Validate required fields (e.g. customer_name)
#     #     if not customer_name:
#     #         return Response(
#     #             {'detail': 'Customer name is required.'},
#     #             status=status.HTTP_400_BAD_REQUEST
#     #         )

#     #     # 2) Create or retrieve the Customer
#     #     customer, _ = Customer.objects.get_or_create(
#     #         name=customer_name,
#     #         defaults={
#     #             'email': customer_email,
#     #             'contact': customer_contact
#     #         }
#     #     )
#     #     # If you want to update existing info, do so here:
#     #     # e.g. customer.email = customer_email or ...
#     #     # customer.save()

#     #     created_feedbacks = []

#     #     # 3) Create each ArcadeFeedback
#     #     for fb_data in feedbacks_data:
#     #         question_id = fb_data.get('question')
#     #         rating = fb_data.get('rating', 0)

#     #         # Validate question exists
#     #         try:
#     #             question_obj = ArcadeQuestion.objects.get(id=question_id)
#     #         except ArcadeQuestion.DoesNotExist:
#     #             return Response(
#     #                 {'detail': f'Question {question_id} does not exist.'},
#     #                 status=status.HTTP_400_BAD_REQUEST
#     #             )

#     #         feedback_obj = ArcadeFeedback.objects.create(
#     #             customer=customer,
#     #             question=question_obj,
#     #             rating=rating
#     #         )
#     #         created_feedbacks.append(feedback_obj)

#     #     # 4) Serialize the newly created feedback objects
#     #     serializer = ArcadeFeedbackSerializer(created_feedbacks, many=True)
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)

#     # def list(self, request, *args, **kwargs):
#     #     # Group feedback by customers
#     #     customers = Customer.objects.prefetch_related('feedbacks__question')

#     #     grouped_data = []
#     #     for customer in customers:
#     #         # Calculate the overall rating for this customer
#     #         feedbacks = customer.feedbacks.all()
#     #         overall_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0

#     #         # Serialize the feedbacks
#     #         serialized_feedbacks = ArcadeFeedbackSerializer(feedbacks, many=True).data

#     #         grouped_data.append({
#     #             "customer_name": customer.name,
#     #             "customer_email": customer.email,
#     #             'customer_contact': customer.contact,
#     #             "overall_rating": round(overall_rating, 2),
#     #             "feedbacks": serialized_feedbacks
#     #         })

#     #     return Response(grouped_data)
class ArcadeFeedbackViewSet(viewsets.ModelViewSet):
    queryset = ArcadeFeedback.objects.select_related('question')
    serializer_class = ArcadeFeedbackSerializer
    def create(self, request, *args, **kwargs):
        customer_name = request.data.get('customer_name')
        customer_email = request.data.get('customer_email', '')
        customer_contact = request.data.get('customer_contact', '')
        feedbacks_data = request.data.get('feedbacks', [])

        if not customer_name:
            return Response(
                {"detail": "Customer name is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not feedbacks_data:
            return Response(
                {"detail": "Feedback data is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_feedbacks = []
        for fb_data in feedbacks_data:
            question_id = fb_data.get("question")
            rating = fb_data.get("rating", 0)

            # Check if question exists
            try:
                question_obj = ArcadeQuestion.objects.get(id=question_id)
            except ArcadeQuestion.DoesNotExist:
                return Response(
                    {"detail": f"Question {question_id} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create feedback entry
            feedback_obj = ArcadeFeedback.objects.create(
                customer_name=customer_name,
                customer_email=customer_email,
                customer_contact=customer_contact,
                question=question_obj,  # Use the validated question object
                rating=rating,
            )
            created_feedbacks.append(feedback_obj)

        # Serialize and return the created feedbacks
        overall_rating = sum(fb.rating for fb in created_feedbacks) / len(created_feedbacks)
        serializer = ArcadeFeedbackSerializer(created_feedbacks, many=True)

        return Response(
            {
                "customer_name": customer_name,
                "customer_email": customer_email,
                "customer_contact": customer_contact,
                "overall_rating": overall_rating,
                "feedbacks": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


    def list(self, request, *args, **kwargs):
        feedbacks = self.get_queryset()
        
        # Group feedback by customer details
        grouped_data = {}
        for fb in feedbacks:
            customer_key = (fb.customer_name, fb.customer_email, fb.customer_contact)
            
            if customer_key not in grouped_data:
                grouped_data[customer_key] = {
                    "customer_name": fb.customer_name,
                    "customer_email": fb.customer_email,
                    "customer_contact": fb.customer_contact,
                    "feedbacks": [],
                }

            grouped_data[customer_key]["feedbacks"].append({
                "id": fb.id,
                "question": fb.question.question,
                "rating": fb.rating,
                "created_at": fb.created_at,
            })
        
        # Add overall rating for each customer group
        for group in grouped_data.values():
            ratings = [fb["rating"] for fb in group["feedbacks"]]
            group["overall_rating"] = sum(ratings) / len(ratings) if ratings else 0

        # Return the grouped data as a list
        return Response(list(grouped_data.values()), status=status.HTTP_200_OK)






# ------------------ Cafe ViewSets ------------------ #
class CafeQuestionViewSet(viewsets.ModelViewSet):
    queryset = CafeQuestion.objects.all()
    serializer_class = CafeQuestionSerializer


class CafeFeedbackViewSet(viewsets.ModelViewSet):
    queryset = CafeFeedback.objects.all()
    serializer_class = CafeFeedbackSerializer





class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerVisitViewSet(viewsets.ModelViewSet):
    queryset = CustomerVisit.objects.all()
    serializer_class = CustomerVisitSerializer