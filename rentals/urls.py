from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rentals import views as rental_views
from django.contrib.auth import views as auth_views

app_name = 'rentals'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('edit-profile/', rental_views.edit_profile, name='edit_profile'),
    path('', rental_views.home, name='home'),
    path('register/', rental_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view( template_name='login.html', redirect_authenticated_user=True ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', rental_views.profile, name='profile'),
    path('cars/', rental_views.car_list, name='cars'),
    path('rent/<int:car_id>/', rental_views.rent_car, name='rent_car'),
    path('admin-dashboard/', rental_views.admin_dashboard, name='admin_dashboard'),
    path('manage-cars/', rental_views.manage_cars, name='manage_cars'),
    path('manage-orders/', rental_views.manage_orders, name='manage_orders'),
    path('add-car/', rental_views.add_car, name='add_car'),
    path('delete-car/<int:car_id>/', rental_views.delete_car, name='delete_car'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)