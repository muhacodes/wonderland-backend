from django.db import models
from django.utils.crypto import get_random_string
from django.db.models.signals import pre_save


# Staff Profile
class Staff(models.Model):
    TASK_TYPE_CHOICES = [
        ('Commercial', 'Commercial'),
        ('Q&A', 'Q&A'),
        ('Giveaway', 'Giveaway'),
        ('Ladies Night', 'Ladies Night'),
        ('Events', 'Events'),
    ]
    role                   = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)
    first_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)  # For phone or email

    def __str__(self):
        return self.first_name


class StaffRoles(models.Model):
    TASK_TYPE_CHOICES = [
        ('Commercial', 'Commercial'),
        ('Q&A', 'Q&A'),
        ('Giveaway', 'Giveaway'),
        ('Ladies Night', 'Ladies Night'),
        ('Challenges', 'Challenges'),
        ('Events', 'Events'),
    ]
    role                   = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)

    def __str__(self):
        return self.role



class StaffProfile(models.Model):
    photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True)
    full_name = models.CharField(max_length=255)  # Full name of the staff member
    role = models.ManyToManyField(StaffRoles, null=True, blank=True)
    department = models.CharField(max_length=250, null=True, blank=True)
    area_of_residence = models.CharField(max_length=255, null=True, blank=True)  # Residence
    start_date = models.DateField( null=True, blank=True)  # Start date of employment
    telephone_number = models.CharField(max_length=15, null=True, blank=True)  # Phone number

    def __str__(self):
        return self.full_name

# Marketing

# Tasks
class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('Commercial', 'Commercial'),
        ('Q&A', 'Q&A'),
        ('Giveaway', 'Giveaway'),
        ('Ladies Night', 'Ladies Night'),
        ('Challenges', 'Challenges'),
        ('Events', 'Events'),
    ]

    start_date                  = models.DateField()
    task_type                   = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)
    publishing                  = models.BooleanField(default=False) # if publishing is false, its automatically shooting
    staff_members               = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.task_type} - {self.start_date}"



# Targets Board
class Target(models.Model):
    date                        = models.DateField(auto_now_add=True)
    target_type                 = models.CharField(max_length=30, choices=[('Marketing' , 'Marketing'), ('Management' , 'Management')])
    target_name                 = models.CharField(max_length=255)
    description                 = models.TextField()
    completed                   = models.BooleanField(default=False)
    deadline                    = models.DateField()
    staff_members               = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.target_name



# Meetings
class Meeting(models.Model):
    MEETING_TYPE_CHOICES = [
        ('SMM', 'Senior Management Meeting'),
        ('MM', 'Management Meeting'),
    ]

    meeting_type                = models.CharField(max_length=50, choices=MEETING_TYPE_CHOICES)
    date                        = models.DateField()
    agenda                      = models.TextField()

    def __str__(self):
        return f"{self.meeting_type} - {self.date}"



from django.db import models


# ------------------ Arcade Models ------------------ #
# Customer model to store user details
class Customer(models.Model):
    name = models.CharField(max_length=250)
    contact = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    children = models.SmallIntegerField(null=True, blank=True)
    last_visit = models.DateField(null=True, blank=True)
    membership = models.BooleanField(null=True, blank=True)
    membership_id = models.CharField(max_length=6, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name

class ArcadeQuestion(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class ArcadeFeedback(models.Model):
    # customer = models.ForeignKey(
    #     Customer, 
    #     on_delete=models.CASCADE, 
    #     related_name='feedbacks',
    #     null=True
    # )
    customer_name   = models.CharField(max_length=250)
    customer_email  = models.EmailField(null=True, blank=True)
    customer_contact = models.CharField(null=True, max_length=25, blank=True)
    question = models.ForeignKey(
        ArcadeQuestion, 
        on_delete=models.CASCADE, 
        related_name='feedbacks'
    )
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name}: {self.question.question} - {self.rating}"



# ------------------ Cafe Models ------------------ #
class CafeQuestion(models.Model):
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class CafeFeedback(models.Model):
    question = models.ForeignKey(
        CafeQuestion, 
        on_delete=models.CASCADE, 
        related_name='feedbacks'
    )
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cafe: {self.question.question} - Rating: {self.rating}"




def generate_membership_id(instance):
    if not instance.membership_id:
        name_part = instance.name[:3].upper() if instance.name else "CST"
        random_part = get_random_string(3, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        instance.membership_id = f"{name_part}{random_part}"


class CustomerVisit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='visits')
    date = models.DateField()
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    children = models.SmallIntegerField()

    def save(self, *args, **kwargs):
        self.customer.last_visit = self.date
        self.customer.save()
        super().save(*args, **kwargs)



def pre_save_customer(sender, instance, *args, **kwargs):
    generate_membership_id(instance)


pre_save.connect(pre_save_customer, sender=Customer)