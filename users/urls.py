from django.urls import path
from .views import home, profile, RegisterView, wallet, clear_balance_changes

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('wallet/', wallet, name='users-wallet'),
    path('clear_balance_changes/', clear_balance_changes, name='clear_balance_changes'),
]
