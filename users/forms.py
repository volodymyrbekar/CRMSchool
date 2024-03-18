from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


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


# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(label="", max_length=40, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
#     last_name = forms.CharField(label="", max_length=40,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    # class Meta:
    #     model = User
    #     fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
    #
    #
    # def __init__(self, *args, **kwargs):
    #     super(SignUpForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['username'].widget.attrs['class'] = 'form-control'
    #     self.fields['username'].widget.attrs['placeholder'] = 'Username'
    #     self.fields['username'].label = ''
    #     self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
    #
    #     self.fields['password1'].widget.attrs['class'] = 'form-control'
    #     self.fields['password1'].widget.attrs['placeholder'] = 'Password'
    #     self.fields['password1'].label = ''
    #     self.fields['password1'].help_text = '<span class="form-text text-muted"><small><ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul></small></span>'
    #
    #     self.fields['password2'].widget.attrs['class'] = 'form-control'
    #     self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
    #     self.fields['password2'].label = ''
    #     self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
    #
