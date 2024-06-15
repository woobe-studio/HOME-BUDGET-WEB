from django.contrib import admin
from .models import Profile, Budget, Category, BalanceChange

admin.site.register(Profile)
admin.site.register(Budget)
admin.site.register(Category)
admin.site.register(BalanceChange)