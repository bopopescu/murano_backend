from rest_framework import serializers
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from .models import Transaction, Category, FeedbackMessage, Product, Order, OrderProduct





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
        fields = ('id', 'name', 'values')

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


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity')


class OrderProductSerializerRetriever(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        depth = 1
        fields = ('product', 'quantity')

class OrderCreateSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('customer', 'products')

    def create(self, validated_data):
        total = 0
        products = validated_data.pop('products')
        customer = validated_data['customer']
        for each in products:
            total += int(each['product'].price) * int(each['quantity'])
        if total > int(customer.personal_points):
            raise serializers.ValidationError('Недостаточно средств')
        customer.personal_points = int(customer.personal_points)-total
        question = Order.objects.create(**validated_data)
        choice_set_serializer = self.fields['products']

        for each in products:
            print(each)
            total += int(each['product'].price) * int(each['quantity'])
            each['order'] = question
        op = choice_set_serializer.create(products)
        question.total = total
        question.save()
        customer.save()
        return question


class OrderSerializer(serializers.ModelSerializer):
    customer = UserFIOSerializer(many=False, read_only=True)
    products = OrderProductSerializerRetriever(source='orderproduct_set', many= True, read_only=True)
    class Meta:
        model = Order

        fields = "__all__"


class OrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'active', 'delivered_at']
        extra = ['id']





