from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from decimal import Decimal


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(null=True, blank=True, default='')
    balance = models.DecimalField(default=Decimal('0.00'), max_digits=12, decimal_places=2)
    categories = models.ManyToManyField('Category', blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

        if self._state.adding:
            description = 'Initial balance'
        else:
            previous_balance = Profile.objects.get(pk=self.pk).balance
            amount_changed = self.balance - previous_balance
            if amount_changed > Decimal('0'):
                description = f'Added ${amount_changed:.2f}'
            elif amount_changed < Decimal('0'):
                description = f'Subtracted ${abs(amount_changed):.2f}'
            else:
                return

        BalanceChange.objects.create(profile=self, amount=self.balance, description=description)


class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Budget"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BalanceChange(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
