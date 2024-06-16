from django.urls import path
from .views import home, profile, RegisterView, wallet, clear_balance_changes, balance_changes, clear_categories, \
    charts, edit_balance_changes

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('wallet/', wallet, name='users-wallet'),
    path('clear-categories/', clear_categories, name='users-clear_categories'),
    path('balance-changes/', balance_changes, name='users-balance_changes'),
    path('clear_balance_changes/', clear_balance_changes, name='users-clear_balance_changes'),
    path('edit_balance_changes/', edit_balance_changes, name='users-edit_balance_changes'),
    path('charts/', charts, name='users-charts'),
]
