from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from decimal import Decimal


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Wallet(models.Model):
    profiles = models.ManyToManyField(Profile, related_name='wallets')
    name = models.CharField(max_length=100)
    balance = models.DecimalField(default=Decimal('0.00'), max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    wallet_type = models.CharField(max_length=20, choices=[('personal', 'Personal'), ('group', 'Group')], default='personal')
    categories = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._state.adding:
            description = 'Initial balance'
        else:
            previous_balance = Wallet.objects.get(pk=self.pk).balance
            amount_changed = self.balance - previous_balance
            if amount_changed > Decimal('0'):
                description = f'Added ${amount_changed:.2f}'
            elif amount_changed < Decimal('0'):
                description = f'Subtracted ${abs(amount_changed):.2f}'
            else:
                return
        BalanceChange.objects.create(wallet=self, amount=self.balance, description=description)

    def get_profiles_display(self):
        return ", ".join([profile.user.username for profile in self.profiles.all()])


class BalanceChange(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='balance_changes', default=None)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=100, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    category_name = models.CharField(max_length=255, blank=True, editable=False)
    timestamp = models.DateTimeField(default=timezone.now, editable=True)

    def save(self, *args, **kwargs):
        if self.category:
            self.category_name = self.category.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.description} - {self.amount}'
