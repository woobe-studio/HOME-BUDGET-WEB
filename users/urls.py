from django.urls import path
from .views import home, profile, RegisterView, wallet, clear_balance_changes, balance_changes, clear_categories, \
    charts, edit_balance_change, delete_balance_change, export_balance_changes, create_wallet, \
    wallet_selection, select_existing_wallet

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('wallet/<int:wallet_id>/', wallet, name='users-wallet'),
    path('wallet_selection/', wallet_selection, name='users-wallet_selection'),
    path('create-wallet/', create_wallet, name='users-create_wallet'),
    path('select_existing_wallet/', select_existing_wallet, name='select_existing_wallet'),
    path('clear-categories/<int:wallet_id>/', clear_categories, name='users-clear_categories'),
    path('balance-changes/<int:wallet_id>/', balance_changes, name='users-balance_changes'),
    path('clear_balance_changes/<int:wallet_id>/', clear_balance_changes, name='users-clear_balance_changes'),
    path('edit_balance_change/<int:wallet_id>/', edit_balance_change, name='users-edit_balance_change'),
    path('delete_balance_change/<int:wallet_id>/', delete_balance_change, name='users-delete_balance_change'),
    path('export_balance_changes/<int:wallet_id>/', export_balance_changes, name='users-export_balance_changes'),
    path('charts/<int:wallet_id>/', charts, name='users-charts'),
]
