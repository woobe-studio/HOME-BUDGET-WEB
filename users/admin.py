from django.contrib import admin
from .models import Profile, Category, BalanceChange

class BalanceChangeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'amount', 'description', 'category', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('profile__user__username', 'description')

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(BalanceChange, BalanceChangeAdmin)