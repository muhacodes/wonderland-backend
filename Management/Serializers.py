from rest_framework import serializers
from .models import Staff, Task, Target, Meeting,StaffProfile, Customer, CustomerVisit


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TargetSerializer(serializers.ModelSerializer):
    # Handles input as IDs

    class Meta:
        model = Target
        fields = '__all__'


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'



from rest_framework import serializers
from .models import (
    ArcadeQuestion,
    ArcadeFeedback,
    CafeQuestion,
    CafeFeedback
)


# ------------------ Arcade Serializers ------------------ #
class ArcadeQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArcadeQuestion
        fields = '__all__'





class ArcadeFeedbackSerializer(serializers.ModelSerializer):
    question = serializers.CharField(source='question.question', read_only=True)

    class Meta:
        model = ArcadeFeedback
        fields = [
            'id', 'customer_name', 'customer_email', 'customer_contact',
            'question', 'rating', 'created_at'
        ]


# ------------------ Cafe Serializers ------------------ #
class CafeQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeQuestion
        fields = '__all__'


class CafeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeFeedback
        fields = '__all__'



class StaffProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()  # Override the roles field

    class Meta:
        model = StaffProfile
        fields = '__all__'

    def get_role(self, obj):
        return [role.role for role in obj.role.all()]  # Return a list of role names



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'contact', 'email', 'children', 'last_visit', 'membership', 'membership_id']
        read_only_fields = ['membership_id']
    

class CustomerVisitSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.name')

    class Meta:
        model = CustomerVisit
        fields = ['id', 'customer', 'customer_name', 'date', 'amount_spent', 'children']