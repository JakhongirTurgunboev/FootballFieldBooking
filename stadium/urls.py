from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, FootballFieldViewSet, FootballFieldImagesViewSet, find_stadium

router = DefaultRouter()
router.register(r'football-field', FootballFieldViewSet, basename='football-field')
router.register(r'football-field-images', FootballFieldImagesViewSet, basename='football-field-images')
router.register(r'booking', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('find/', find_stadium, name='find')
]