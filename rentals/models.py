from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    mileage = models.IntegerField()
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    seats = models.IntegerField()
    image = models.ImageField(upload_to='car_images/', null=True, blank=True)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class RentalOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    order_date = models.DateTimeField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)

    def __str__(self):
        return f"Order #{self.id} - {self.car} rented by {self.user}"

    def calculate_total_cost(self):
        days = (self.end_date - self.start_date).days
        return days * self.car.daily_rate

    def save(self, *args, **kwargs):
        if not self.total_cost:
            self.total_cost = self.calculate_total_cost()
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        days = (self.end_date - self.start_date).days
        return days * self.car.daily_rate

    def save(self, *args, **kwargs):
        if not self.total_price:  # Jeśli pole nie jest ustawione
            self.total_price = self.calculate_total()
        super().save(*args, **kwargs)
