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
from Sales.views import SaleViewSet, ExpenseViewSet
from Liabilities.views import LiabilityViewSet

# Create a router and register viewsets
router = DefaultRouter()

router.register(r'sales', SaleViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'liability', LiabilityViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/api', include('account.urls')), 
    path('auth/api/', include('account.urls')),
    path('api/', include(router.urls)),  # Include the router's URLs
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
