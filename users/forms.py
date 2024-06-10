from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile, Category


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


class WalletForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    description = forms.CharField(label='Description', max_length=100, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category", required=False)
    new_category = forms.CharField(label='New Category', max_length=30, required=False)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        category = cleaned_data.get("category")
        description = cleaned_data.get("description")
        new_category = cleaned_data.get("new_category")

        if new_category and not category:
            del self.errors['category']
        if not description:
            if amount >= 0:
                cleaned_data["description"] = "Income"
            else:
                cleaned_data["description"] = "Expense"
        print(cleaned_data)
        return cleaned_data
