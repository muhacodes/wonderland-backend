from django.contrib import admin

from .models import Staff, Task, Target,  Meeting, ArcadeFeedback, CafeFeedback, ArcadeQuestion, CafeQuestion, Customer, StaffProfile, StaffRoles

# Register your models here.



admin.site.register(Staff)
admin.site.register(Task)
admin.site.register(Target)
admin.site.register(Meeting)

admin.site.register(CafeFeedback)
admin.site.register(CafeQuestion)
admin.site.register(ArcadeQuestion)
admin.site.register(ArcadeFeedback)
admin.site.register(Customer)
admin.site.register(StaffProfile)
admin.site.register(StaffRoles)