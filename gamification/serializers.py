from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import Transaction, Category





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', "share_points", "personal_points", 'profile', 'position','is_staff', 'is_teamlead')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'password', "share_points", "personal_points", 'profile', 'position','is_staff', 'is_teamlead')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
