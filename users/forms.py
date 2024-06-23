from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile, Category


class DraculaTextInput(forms.TextInput):
    """
    A custom TextInput widget with Dracula theme.

    This widget sets the class attribute to 'form-control' and custom styles for background color and text color
    to achieve the Dracula theme.

    Example:
        form_field = forms.CharField(widget=DraculaTextInput())

    Attributes:
        None

    Methods:
        __init__: Initializes the DraculaTextInput widget with the specified attributes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the DraculaTextInput widget with the specified attributes.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Keyword Args:
            Any additional keyword arguments supported by forms.TextInput.

        Returns:
            None
        """
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'class': 'form-control',
            'style': 'background-color: #282a36; color: #f8f8f2;'
        })
        super().__init__(*args, **kwargs)


class DraculaPasswordInput(forms.PasswordInput):
    """
    A custom PasswordInput widget with Dracula theme.

    This widget sets the class attribute to 'form-control' and custom styles for background color and text color
    to achieve the Dracula theme.

    Example:
        form_field = forms.CharField(widget=DraculaPasswordInput())

    Attributes:
        None

    Methods:
        __init__: Initializes the DraculaPasswordInput widget with the specified attributes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the DraculaPasswordInput widget with the specified attributes.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Keyword Args:
            Any additional keyword arguments supported by forms.PasswordInput.

        Returns:
            None
        """
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'class': 'form-control',
            'style': 'background-color: #282a36; color: #f8f8f2;'
        })
        super().__init__(*args, **kwargs)


class RegisterForm(UserCreationForm):
    """
    A custom UserCreationForm for user registration with Dracula theme.

    This form extends the UserCreationForm and customizes the fields with DraculaTextInput
    and DraculaPasswordInput widgets to achieve the Dracula theme.

    Example:
        form = RegisterForm()

    Attributes:
        None

    Methods:
        None
    """

    first_name = forms.CharField(max_length=100, required=True,
                                 widget=DraculaTextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, required=True,
                                widget=DraculaTextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=100, required=True,
                               widget=DraculaTextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(required=True,
                             widget=DraculaTextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=50, required=True,
                                widget=DraculaPasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=50, required=True,
                                widget=DraculaPasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    """
    A custom AuthenticationForm for user login with Dracula theme.

    This form extends the AuthenticationForm and customizes the fields with DraculaTextInput
    and DraculaPasswordInput widgets to achieve the Dracula theme.

    Example:
        form = LoginForm()

    Attributes:
        None

    Methods:
        None
    """

    username = forms.CharField(max_length=100, required=True,
                               widget=DraculaTextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=50, required=True,
                               widget=DraculaPasswordInput(attrs={'placeholder': 'Password'}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User


class UpdateUserForm(forms.ModelForm):
    """
    A custom ModelForm for updating user information with Dracula theme.

    This form allows users to update their username and email with DraculaTextInput
    widgets to achieve the Dracula theme.

    Example:
        form = UpdateUserForm()

    Attributes:
        None

    Methods:
        None
    """

    username = forms.CharField(max_length=100, required=True,
                               widget=DraculaTextInput())
    email = forms.EmailField(required=True,
                             widget=DraculaTextInput())

    class Meta:
        model = User
        fields = ['username', 'email']


class DraculaTextarea(forms.Textarea):
    """
    A custom Textarea widget with Dracula theme.

    This widget sets the class attribute to 'form-control' and custom styles for background color and text color
    to achieve the Dracula theme.

    Example:
        form_field = forms.CharField(widget=DraculaTextarea())

    Attributes:
        None

    Methods:
        __init__: Initializes the DraculaTextarea widget with the specified attributes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the DraculaTextarea widget with the specified attributes.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Keyword Args:
            Any additional keyword arguments supported by forms.Textarea.

        Returns:
            None
        """
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'class': 'form-control',
            'style': 'background-color: #282a36; color: #f8f8f2;'
        })
        super().__init__(*args, **kwargs)


class UpdateProfileForm(forms.ModelForm):
    """
    A custom ModelForm for updating user profile information with Dracula theme.

    This form allows users to update their avatar and bio with DraculaTextarea
    widget for bio field and basic file input widget for avatar field.

    Example:
        form = UpdateProfileForm()

    Attributes:
        None

    Methods:
        None
    """

    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(required=False, widget=DraculaTextarea(attrs={'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class WalletForm(forms.Form):
    """
    A form for adding transactions to the wallet.

    This form allows users to add transactions with fields for amount, description, category, and new category.

    Example:
        form = WalletForm()

    Attributes:
        None

    Methods:
        clean: Custom form validation method to handle special cases.
    """

    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    description = forms.CharField(label='Description', max_length=100, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category", required=False)
    new_category = forms.CharField(label='New Category', max_length=30, required=False)

    def clean(self):
        """
        Custom form validation method to handle special cases.

        If a new category is provided without selecting an existing category, it clears errors.
        If description is not provided, it sets a default value based on the amount (Income or Expense).

        Returns:
            dict: Cleaned data dictionary.
        """
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        category = cleaned_data.get("category")
        description = cleaned_data.get("description")
        new_category = cleaned_data.get("new_category")

        if new_category and not category or 'category' in self.errors:
            self.errors.clear()
        if not description:
            if amount >= 0:
                cleaned_data["description"] = "Income"
            else:
                cleaned_data["description"] = "Expense"
        return cleaned_data
