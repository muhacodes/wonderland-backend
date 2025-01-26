"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from Sales.views import SaleViewSet, ExpenseViewSet, InventoryItemViewSet, CategoryViewSet, SubCategoryViewSet
from Liabilities.views import LiabilityViewSet
from Bookings.views import BookingViewSet
from Management.views import StaffViewSet, TaskViewSet, TargetViewSet, MeetingViewSet, ArcadeQuestionViewSet, ArcadeFeedbackViewSet, CafeQuestionViewSet,CafeFeedbackViewSet, StaffProfileViewSet, CustomerViewSet,CustomerVisitViewSet

# Create a router and register viewsets
router = DefaultRouter()

router.register('sales', SaleViewSet)
router.register('expenses', ExpenseViewSet)
router.register('liability', LiabilityViewSet)
router.register('booking', BookingViewSet)

router.register('customer', CustomerViewSet, basename='customer')
router.register('customer-visits', CustomerVisitViewSet, basename='visit')

router.register('staff', StaffViewSet)
router.register('tasks', TaskViewSet)
router.register('targets', TargetViewSet)
router.register('meetings', MeetingViewSet)
router.register('arcade-question', ArcadeQuestionViewSet)
router.register('arcade-feedback', ArcadeFeedbackViewSet)
router.register('cafe-question', CafeQuestionViewSet)
router.register('cafe-feedback', CafeFeedbackViewSet)
router.register('staff-profile', StaffProfileViewSet)
router.register('inventory', InventoryItemViewSet)

router.register('category', CategoryViewSet)
router.register('subcategory', SubCategoryViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/api', include('account.urls')), 
    path('auth/api/', include('account.urls')),
    path('api/', include(router.urls)),  # Include the router's URLs
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
