from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.businesses.views import BusinessViewSet, BusinessCategoryViewSet

app_name = 'businesses'

router = DefaultRouter()
router.register(r'', BusinessViewSet, basename='business')
router.register(r'categories', BusinessCategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
