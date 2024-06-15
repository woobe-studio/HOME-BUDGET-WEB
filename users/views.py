from scripts.custom_scripts import *

from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, WalletForm
from .models import BalanceChange, Category


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
    categories = sorted(profile.categories.all(), key=lambda c: c.name.lower())
    return render(request, 'users/wallet.html', {'form': form, 'balance': formatted_balance, 'categories': categories})


@login_required
def clear_categories(request):
    profile = request.user.profile
    profile.categories.clear()
    default_categories = ['Entertainment', 'Food', 'Transportation', 'Health', 'Shopping', 'Savings']
    default_categories.sort()
    for category_name in default_categories:
        category_obj, created = Category.objects.get_or_create(name=category_name)
        profile.categories.add(category_obj)

    messages.success(request, "All categories have been cleared and default categories have been added.")
    return redirect('users-wallet')

@login_required
def balance_changes(request):
    profile = request.user.profile
    sort_by = request.GET.get('sort_by')
    filter_by = request.GET.get('filter_by')
    selected_category = request.GET.get('selected_category')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    day = request.GET.get('day')
    day_name = request.GET.get('day_name')
    month_name = request.GET.get('month')
    year = request.GET.get('year')

    try:
        min_amount = Decimal(min_amount) if min_amount else None
    except (InvalidOperation, ValueError):
        min_amount = None

    try:
        max_amount = Decimal(max_amount) if max_amount else None
    except (InvalidOperation, ValueError):
        max_amount = None

    try:
        day = int(day) if day else None
    except (ValueError, TypeError):
        day = None

    try:
        month = get_months().get(month_name) if month_name else None
    except AttributeError:
        month = None

    try:
        year = int(year) if year else None
    except (ValueError, TypeError):
        year = None

    years = get_years()
    months = list(get_months().keys())
    days = get_days(datetime.now().year, month)
    day_names = get_day_names()

    try:
        day_name_week = (day_names.index(day_name) + 2 ) % 7
    except ValueError:
        day_name_week = None

    sorted_changes = BalanceChange.objects.filter(profile=profile)

    category_filter_display = 'none'
    amount_filter_display = 'none'
    date_filter_display = 'none'
    if filter_by not in ['SelectFilter', 'SelectAllFilters', None, 'None', ''] and selected_category not in ['', 'Select Category']:
        category_filter_display = 'block'
    else:
        category_filter_display = 'none'
        filter_by = 'SelectFilter'

    if day is not None or month_name not in [None, 'None', ''] or year is not None or day_name_week not in [None, 'None', '']:
        date_filter_display = 'block'
    else:
        date_filter_display = 'none'
        filter_by = 'SelectFilter'

    if selected_category and selected_category != "None":
        category = get_object_or_404(Category, name=selected_category)
        sorted_changes = sorted_changes.filter(category=category)
    if min_amount is not None:
        sorted_changes = sorted_changes.filter(amount__gte=min_amount)
        amount_filter_display = 'block'
    if max_amount is not None:
        sorted_changes = sorted_changes.filter(amount__lte=max_amount)
        amount_filter_display = 'block'

    if year is not None:
        sorted_changes = sorted_changes.filter(timestamp__year=year)
    if month is not None:
        sorted_changes = sorted_changes.filter(timestamp__month=month)
    if day_name_week is not None:
        sorted_changes = sorted_changes.filter(timestamp__week_day=day_name_week)
    if day is not None:
        sorted_changes = sorted_changes.filter(timestamp__day=day)

    if sort_by == 'AscendingCost':
        balance_changes = sorted_changes.order_by('amount')
    elif sort_by == 'DescendingCost':
        balance_changes = sorted_changes.order_by('-amount')
    elif sort_by == 'DateOldestFirst':
        balance_changes = sorted_changes.order_by('timestamp')
    elif sort_by == 'DateNewestFirst':
        balance_changes = sorted_changes.order_by('-timestamp')
    elif sort_by == 'AscendingCategoryName':
        balance_changes = sorted_changes.order_by('category__name')
    elif sort_by == 'DescendingCategoryName':
        balance_changes = sorted_changes.order_by('-category__name')
    else:
        balance_changes = sorted_changes.order_by('-timestamp')
        sort_by = 'SelectSort'

    paginator = Paginator(balance_changes, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = sorted(profile.categories.all(), key=lambda c: c.name.lower())
    return render(request, 'users/balance_changes.html', {
        'page_obj': page_obj,
        'sort_by': sort_by,
        'filter_by': filter_by,
        'selected_category': selected_category,
        'categories': categories,
        'min_amount': min_amount,
        'max_amount': max_amount,
        'category_filter_display': category_filter_display,
        'amount_filter_display': amount_filter_display,
        'date_filter_display': date_filter_display,
        'years': years,
        'months': months,
        'days': days,
        'day_names': day_names,
        'year': str(year),
        'month': month_name,
        'day': str(day),
        'day_name': day_name,
    })


@login_required
def clear_balance_changes(request):
    profile = request.user.profile
    BalanceChange.objects.filter(profile=profile).delete()
    messages.success(request, "All balance change history have been cleared.")
    return redirect('users-balance_changes')


@login_required
def charts(request):
    profile = request.user.profile
    return render(request, 'users/charts.html', {})
