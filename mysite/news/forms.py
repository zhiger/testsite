from django import forms
from .models import News
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
import re


# class NewsForm(forms.Form):
# """ ФОРМА НЕ СВЯЗАНОЙ МОДЕЛЮ """
# title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput(attrs={'class':"form-control"}))
# content = forms.CharField(label='Контент', widget=forms.Textarea(attrs={'class': "form-control", 'rows':5}))
# category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label="", widget=forms.Select(attrs={'class': "form-control"}))
# is_published = forms.BooleanField(label='Опубликовано')


class NewsForm(forms.ModelForm):
    """ ФОРМА СВЯЗАНОЙ МОДЕЛЮ """

    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control"}),
            'content': forms.Textarea(attrs={'class': "form-control", 'rows': 5}),
            'category': forms.Select(attrs={'class': "form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Называние не должно начинаться с цифры')
        return title


class UserRegisterForm(UserCreationForm):
    # можно поставить 'autocomplete': 'off' и тогда не будеть придлогатся подсказки
    # help_text - Аргумент help_text позволяет указать описание для поля.
    # Если вы укажете help_text, он будет показан около поля при отображении формы
    # attrs - Словарь, содержащий атрибуты HTML, которые необходимо определить для отображаемого компонента.
    username = forms.CharField(max_length=150,
                               help_text='Имя пользователя должно быть менее 150 символов',
                               label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=150, label='E-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=150,
                                help_text='Пороль должен быть более 8 символов', label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=150, label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема письма',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()
