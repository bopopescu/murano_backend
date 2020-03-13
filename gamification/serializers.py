from rest_framework import serializers
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from .models import Transaction, Category, FeedbackMessage





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', "share_points", "personal_points", 'profile', 'position','is_staff', 'is_teamlead')

        # fields = '__all__'

class UserFIOSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email')

        # fields = '__all__'

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'password', "share_points", "personal_points", 'profile', 'position','is_staff', 'is_teamlead')
        extra_kwargs = {'email': {'validators': [EmailValidator, ]},}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class FeedbackMessageSerializer(serializers.ModelSerializer):
    # author = UserSerializer
    # author = UserFIOSerializer(many=False, read_only=True)
    author = UserFIOSerializer(many=False, read_only=True)
    class Meta:
        model = FeedbackMessage
        exclude = []
        fields = '__all__'


class CreateFeedbackMessageSerializer(serializers.ModelSerializer):
    # author = UserSerializer
    # author = UserFIOSerializer(many=False, read_only=True)
    # author = UserFIOSerializer(many=False, read_only=True)
    class Meta:
        model = FeedbackMessage
        exclude = []
        fields = '__all__'