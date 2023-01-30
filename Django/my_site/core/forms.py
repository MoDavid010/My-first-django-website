from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.datetime_safe import datetime

from .models import CustomUser


class SignupForm(UserCreationForm):
    birth_date = forms.DateField(label='Дата рождения', input_formats=['%d-%m-%Y'],
                                 widget=forms.DateInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'dd-mm-yyyy',
                                     }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'birth_date', 'avatar')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Введите емейл!')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким адресом уже существует!')
        return email


class UpdateProfileForm(forms.ModelForm):
    birth_date = forms.DateField(label='Дата рождения', input_formats=['%d-%m-%Y'],
                                 widget=forms.SelectDateWidget(
                                     years=range(datetime.now().year - 70, datetime.now().year + 1), attrs={
                                         'class': 'form-control',
                                         'placeholder': 'dd-mm-yyyy',
                                     }))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'birth_date', 'about', 'avatar'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget.years = range(datetime.now().year - 70, datetime.now().year + 1)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Введите емейл!')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким адресом уже существует!')
        return email