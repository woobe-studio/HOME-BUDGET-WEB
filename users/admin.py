from django.contrib import admin
from .models import Profile, Category, Wallet, BalanceChange


class BalanceChangeInline(admin.TabularInline):
    model = BalanceChange
    extra = 0


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_profiles_display', 'balance', 'currency', 'wallet_type', 'created_at')
    list_filter = ('profiles', 'currency', 'wallet_type', 'created_at')
    search_fields = ['name', 'profiles__user__username']
    inlines = [BalanceChangeInline]


@admin.register(BalanceChange)
class BalanceChangeAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'description', 'category_name', 'timestamp')
    list_filter = ('wallet__name', 'category', ('timestamp', admin.DateFieldListFilter))
    search_fields = ['wallet__name', 'description', 'category__name']
    readonly_fields = ('category_name',)  # Make category_name field read-only in admin
    date_hierarchy = 'timestamp'  # Add date hierarchy for easy navigation
    ordering = ['-timestamp']  # Default ordering by timestamp


admin.site.register(Profile)
admin.site.register(Category)
