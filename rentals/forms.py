
from .models import User, Car, RentalOrder
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


from django import forms
from .models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': ' '
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add form-control class and placeholder to all fields
        for field_name, field in self.fields.items():
            if field_name != 'address':  # address already handled
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': ' '
                })

            # Add specific attributes for password fields
            if field_name in ['password1', 'password2']:
                field.widget.attrs.update({
                    'autocomplete': 'new-password'
                })

        # Customize help texts
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = '150 characters or fewer. Letters, digits and @/./+/-/_ only.'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class RentalOrderForm(forms.ModelForm):
    class Meta:
        model = RentalOrder
        fields = ['start_date', 'end_date', 'pickup_location', 'dropoff_location']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date < timezone.now().date():
                raise forms.ValidationError("Start date cannot be in the past.")
            if end_date <= start_date:
                raise forms.ValidationError("End date must be after start date.")

        return cleaned_data
