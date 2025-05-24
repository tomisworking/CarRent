from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, RentalOrder
from .forms import UserRegisterForm, CarForm, RentalOrderForm, UserProfileForm


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})



def car_list(request):
    cars = Car.objects.filter(available=True)
    return render(request, 'cars.html', {'cars': cars})


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True
            user.save()
            username = form.cleaned_data.get('username')
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    rentals = RentalOrder.objects.filter(user=request.user) \
        .select_related('car') \
        .order_by('-start_date')

    # Debugowanie - sprawdź czy ceny są prawidłowe
    for rental in rentals:
        print(f"Rental ID: {rental.id}")
        print(f"Car Daily Rate: {rental.car.daily_rate}")
        print(f"Calculated Total: {rental.total_price}")

    return render(request, 'profile.html', {
        'user': request.user,
        'rentals': rentals
    })


def car_list(request):
    cars = Car.objects.filter(available=True)
    return render(request, 'cars.html', {'cars': cars})


@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = RentalOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.car = car
            order.total_cost = order.calculate_total_cost()
            order.save()
            messages.success(request, 'Your rental request has been submitted!')
            return redirect('profile')
    else:
        # Default rental period: tomorrow for 3 days
        initial_data = {
            'start_date': timezone.now().date() + timedelta(days=1),
            'end_date': timezone.now().date() + timedelta(days=4),
            'pickup_location': 'Main Office',
            'dropoff_location': 'Main Office',
        }
        form = RentalOrderForm(initial=initial_data)

    return render(request, 'rent_car.html', {'car': car, 'form': form})


# Admin views
def is_admin(user):
    return user.is_authenticated and not user.is_customer


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')


@login_required
@user_passes_test(is_admin)
def manage_cars(request):
    cars = Car.objects.all()
    return render(request, 'admin/manage_cars.html', {'cars': cars})


@login_required
@user_passes_test(is_admin)
def manage_orders(request):
    orders = RentalOrder.objects.all().order_by('-order_date')
    return render(request, 'admin/manage_orders.html', {'orders': orders})


@login_required
@user_passes_test(is_admin)
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car added successfully!')
            return redirect('manage_cars')
    else:
        form = CarForm()
    return render(request, 'admin/add_car.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Car deleted successfully!')
        return redirect('manage_cars')
    return render(request, 'admin/delete_car.html', {'car': car})
