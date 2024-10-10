from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from centers.models import Center
from .models import CustomUser
from .widgets import CenterSelectWidget


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ім\'я'}))
    last_name = forms.CharField(label="", max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}))
    role = forms.ChoiceField(choices=CustomUser.ROLES, label='Роль')
    username = forms.CharField(label="Логін", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}))  # Додано поле для введення логіну користувача

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        print("Attempting to create user with data:", cleaned_data)
        if self.errors:
            print("Validation errors:", self.errors)
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    centers = forms.ModelMultipleChoiceField(
        queryset=Center.objects.all(),
        required=False,
        widget=CenterSelectWidget('Centers', is_stacked=False),
        label=''
    )

    class Meta:
        model = CustomUser
        fields = '__all__'
