from django.urls import path
from .views import ProfileCreateView, ProfileUpdateView

app_name = 'user_management'
urlpatterns = [
    path('add/', ProfileCreateView.as_view(), name='profile_create'),
    path('<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
]