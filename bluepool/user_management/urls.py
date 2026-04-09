from django.urls import path, include
from .views import ProfileCreateView, ProfileUpdateView, NewProfileCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'user_management'
urlpatterns = [
    path('add/', ProfileCreateView.as_view(), name='profile_create'),
    path('<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
    # new authentication flow starting from here
    path('register/', NewProfileCreateView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('user-auth/', include("rest_framework.urls")),
]