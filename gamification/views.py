
from rest_framework import viewsets
from gamification.serializers import UserSerializer, TransactionSerializer, CategorySerializer
from django.contrib.auth import get_user_model
from  .models import Category, Transaction
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseBadRequest
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsStaffOrReadOnly, IsOwnerOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = IsOwnerOrReadOnly,

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = IsStaffOrReadOnly,


class TransactionsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            from_user = request.data['from_user']
            to_user = request.data['to_user']
            amount = int(request.data['amount'])
            comment = request.data['comment']
            category_id = request.data['category']
            From_User = get_user_model().objects.get(pk=from_user)
            To_User = get_user_model().objects.get(pk=to_user)
            if int(From_User.share_points)< amount:
                return HttpResponseBadRequest({'Недостаточно средств'})
            # проверка на статус пользователя добавить

            To_User.personal_points = str(int(To_User.personal_points) + amount)
            From_User.share_points = str(int(From_User.share_points) - amount)
            To_User.save()
            From_User.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)