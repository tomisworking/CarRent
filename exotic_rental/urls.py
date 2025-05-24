"""
URL configuration for exotic_rental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from rentals import views as rental_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', rental_views.home, name='home'),
    path('', include('rentals.urls')),
    path('register/', rental_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Updated logout
    path('profile/', rental_views.profile, name='profile'),
    path('edit-profile/', rental_views.edit_profile, name='edit_profile'),
    path('cars/', rental_views.car_list, name='cars'),  # Cars page
    path('rent/<int:car_id>/', rental_views.rent_car, name='rent_car'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)