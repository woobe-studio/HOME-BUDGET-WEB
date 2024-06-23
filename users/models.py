from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from decimal import Decimal


class Profile(models.Model):
    """
    Model representing user profiles.

    This model extends the built-in User model to add additional fields such as avatar and bio.

    Attributes:
        user (User): The associated user object.
        avatar (ImageField): The profile picture of the user.
        bio (TextField): The biography of the user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        """
        String representation of the profile.
        """
        return self.user.username

    def save(self, *args, **kwargs):
        """
        Overrides the save method to resize the avatar image to a maximum of 100x100 pixels.
        """
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Category(models.Model):
    """
    Model representing categories that can be associated with transactions or other objects.

    Attributes:
        name (CharField): The name of the category.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        """
        String representation of the category.
        """
        return self.name


class Wallet(models.Model):
    """
    Model representing a wallet in the application.

    Attributes:
        profiles (ManyToManyField): Profiles associated with the wallet.
        name (CharField): The name of the wallet.
        balance (DecimalField): The balance of the wallet.
        currency (CharField): The currency of the wallet.
        wallet_type (CharField): The type of the wallet (personal or group).
        categories (ManyToManyField): Categories associated with the wallet.
        created_at (DateTimeField): The timestamp when the wallet was created.
    """

    profiles = models.ManyToManyField('Profile', related_name='wallets')
    name = models.CharField(max_length=100)
    balance = models.DecimalField(default=Decimal('0.00'), max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    wallet_type = models.CharField(max_length=20, choices=[('personal', 'Personal'), ('group', 'Group')], default='personal')
    categories = models.ManyToManyField('Category', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the wallet.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Override the save method to create a balance change record when the wallet is saved.
        """
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
        """
        Get a comma-separated list of profiles associated with the wallet.
        """
        return ", ".join([profile.user.username for profile in self.profiles.all()])


class BalanceChange(models.Model):
    """
    Model representing a change in the balance of a wallet.

    Attributes:
        wallet (ForeignKey): The wallet associated with the balance change.
        creation_user (CharField): The user responsible for the balance change.
        amount (DecimalField): The amount changed in the balance.
        description (CharField): Description of the balance change.
        category (ForeignKey): The category associated with the balance change.
        category_name (CharField): The name of the associated category (cached for efficiency).
        timestamp (DateTimeField): The timestamp of the balance change.
    """

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='balance_changes', default=None)
    creation_user = models.CharField(max_length=100, default='you')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=100, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    category_name = models.CharField(max_length=255, blank=True, editable=False)
    timestamp = models.DateTimeField(default=timezone.now, editable=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to set the category name based on the associated category.
        """
        if self.category:
            self.category_name = self.category.name
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the balance change.
        """
        return f'{self.description} - {self.amount}'