from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile


class DraculaTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'form-control', 'style': 'background-color: #282a36; color: #f8f8f2;'})
        super().__init__(*args, **kwargs)


class DraculaPasswordInput(forms.PasswordInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'form-control', 'style': 'background-color: #282a36; color: #f8f8f2;'})
        super().__init__(*args, **kwargs)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=DraculaTextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=DraculaTextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=DraculaTextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(required=True,
                             widget=DraculaTextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=DraculaPasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=DraculaPasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=DraculaTextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=DraculaPasswordInput(attrs={'placeholder': 'Password'}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=DraculaTextInput())
    email = forms.EmailField(required=True,
                             widget=DraculaTextInput())

    class Meta:
        model = User
        fields = ['username', 'email']


class DraculaTextarea(forms.Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'form-control', 'style': 'background-color: #282a36; color: #f8f8f2;'})
        super().__init__(*args, **kwargs)


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(required=False, widget=DraculaTextarea(attrs={'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
