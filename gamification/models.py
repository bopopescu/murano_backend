from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True,)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    objects = CustomUserManager()

    profile = models.TextField(default="Blank")
    position = models.CharField(max_length=25, default="Должность не указана")
    share_points = models.CharField(max_length=10, default=0)
    personal_points = models.CharField(max_length=10, default=0)
    is_teamlead = models.BooleanField(default=0)


    # image = models.ImageField(upload_to='profile_image', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


    # REQUIRED_FIELDS = ['first_name', 'last_name', "status", "is_staff", "points", "profile"]

class Category(models.Model):
    name = models.CharField(max_length=64)

class Transaction(models.Model):

    # ignore when delete not cascade!
    from_user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="to_user")
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    comment = models.TextField(default="")
    amount = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

# class Item(models.Model):
#     name = models.CharField(max_length=64)
#     description = models.TextField(default="")
#     price = models.CharField(max_length=8)
#     quantity = models.CharField(max_length=8)
#     in_stock = models.BooleanField(default=10)
#     разобраться с пикчами

class FeedbackMessage(models.Model):
    topic = models.CharField(max_length=64)
    text = models.TextField()
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    closed = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
