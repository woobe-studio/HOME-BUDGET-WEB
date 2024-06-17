import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from django.db.models.functions import ExtractMonth

from scripts.custom_scripts import *
from scripts.custom_classes import *

from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UpdateUserForm, UpdateProfileForm, WalletForm
from .models import BalanceChange, Category


def home(request):
    return render(request, 'users/home.html')


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

    category_filter_display = 'block'
    amount_filter_display = 'block'
    date_filter_display = 'block'
    if selected_category and selected_category != "None":
        category = get_object_or_404(Category, name=selected_category)
        sorted_changes = sorted_changes.filter(category=category)
    if min_amount is not None:
        sorted_changes = sorted_changes.filter(amount__gte=min_amount)
    if max_amount is not None:
        sorted_changes = sorted_changes.filter(amount__lte=max_amount)

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
def edit_balance_change(request):
    profile = request.user.profile
    if request.method == 'POST':
        edit_id = request.POST.get('edit-id')
        edit_description = request.POST.get('edit-description')
        edit_category = request.POST.get('edit-category')
        try:
            balance_change = BalanceChange.objects.get(id=edit_id, profile=profile)
            if edit_description:
                balance_change.description = edit_description
            if edit_category:
                category = Category.objects.get(name=edit_category)
                balance_change.category = category

            balance_change.save()
            messages.success(request, "Balance Change has been edited successfully.")
        except BalanceChange.DoesNotExist:
            messages.error(request, "Balance Change not found.")
        except Category.DoesNotExist:
            messages.error(request, "Category not found.")
        except InvalidOperation:
            messages.error(request, "Invalid amount entered.")

        return redirect('users-balance_changes')


@login_required
def delete_balance_change(request):
    profile = request.user.profile
    if request.method == 'POST':
        delete_id = request.POST.get('delete-id')
        try:
            balance_change = BalanceChange.objects.get(id=delete_id, profile=profile)
            deleted_amount = balance_change.amount
            balance_change.delete()
            profile.balance += deleted_amount
            profile.save()
            messages.success(request, "Balance Change has been deleted successfully.")
        except BalanceChange.DoesNotExist:
            messages.error(request, "Balance Change not found.")

        return redirect('users-balance_changes')


@login_required
def charts(request):
    profile = request.user.profile

    # Retrieve all balance changes for the user profile
    balance_changes = BalanceChange.objects.filter(profile=profile)

    # Initialize income and expense data arrays
    income_data = [0] * 12
    expense_data = [0] * 12

    # Populate income and expense data arrays for each balance change
    for change in balance_changes:
        month_index = change.timestamp.month - 1
        if change.amount > 0:
            income_data[month_index] += change.amount
        else:
            expense_data[month_index] += abs(change.amount)

    # Prepare data to be passed to the template
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    data = {
        'months': months,
        'income_data': income_data,
        'expense_data': expense_data,
    }

    serialized_data = json.dumps(data, cls=DjangoJSONEncoder)

    return render(request, 'users/charts.html', {'data': serialized_data})
