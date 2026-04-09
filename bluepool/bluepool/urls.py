"""
URL configuration for bluepool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from user_management.views import NewProfileCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import homepage

app_name = 'bluepool'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('', homepage, name='homepage'),
    path('account/', include('django.contrib.auth.urls')),
    path('profile/', include('user_management.urls', namespace='profile')),
    path('rideposting/', include('rideposting.urls', namespace='rideposting')),
    # new authentication flow starting from here
    path('user/', include('user_management.urls'), name='user')
]
