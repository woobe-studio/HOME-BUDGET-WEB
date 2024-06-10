from decimal import Decimal

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, WalletForm
from .models import BalanceChange, Profile, Category


def home(request):
    return render(request, 'users/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)

            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def wallet(request):
    profile = request.user.profile
    form = WalletForm()
    if request.method == 'POST':
        if request.POST.get('action') == 'update_funds':
            form = WalletForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data.get('amount')
                description = form.cleaned_data.get('description')
                category = form.cleaned_data.get('category')
                new_category = form.cleaned_data.get('new_category')
                if new_category:
                    category_obj, created = Category.objects.get_or_create(name=new_category)
                    profile.categories.add(category_obj)
                elif category:
                    category_obj = category
                    profile.categories.add(category_obj)
                else:
                    messages.error(request, 'No category was selected')
                    return redirect('users-wallet')
                if amount != Decimal('0'):
                    if amount < Decimal('0'):
                        if profile.balance >= abs(amount):
                            profile.balance += amount
                            profile.save()
                            BalanceChange.objects.create(profile=profile, amount=amount, description=description, category=category_obj)
                            messages.success(request, f'Balance updated successfully: ${amount:.2f} | Category: {category_obj.name} | Description: {description}')
                        else:
                            messages.error(request, 'Insufficient balance for the transaction')
                    else:
                        profile.balance += amount
                        profile.save()
                        BalanceChange.objects.create(profile=profile, amount=amount, description=description, category=category_obj)
                        messages.success(request, f'Balance updated successfully: ${amount:.2f} | Category: {category_obj.name} | Description: {description}')
                else:
                    messages.error(request, 'Amount must be non-zero to update the balance')
                return redirect('users-wallet')
        elif request.POST.get('action') == 'clear_categories':
            profile.categories.clear()
            messages.success(request, 'Categories cleared successfully')
            return redirect('users-wallet')
    formatted_balance = f'{profile.balance:.2f}'
    balance_changes = BalanceChange.objects.filter(profile=profile)
    categories = profile.categories.all()
    return render(request, 'users/wallet.html', {'form': form, 'balance': formatted_balance, 'balance_changes': balance_changes, 'categories': categories})


@login_required
def clear_balance_changes(request):
    profile = request.user.profile

    BalanceChange.objects.filter(profile=profile).delete()

    return redirect('users-wallet')


@login_required
def clear_categories(request):
    profile = request.user.profile
    Category.objects.all().delete()
    default_categories = ['Entertainment', 'Food', 'Transportation', 'Health', 'Shopping', 'Savings']
    for new_category in default_categories:
        category_obj, created = Category.objects.get_or_create(name=new_category)
        profile.categories.add(category_obj)

    messages.success(request, "All categories have been cleared and default categories have been added.")
    return redirect('users-wallet')