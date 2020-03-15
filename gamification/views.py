
from rest_framework import viewsets
from gamification.serializers import UserSerializer, TransactionSerializer, CategorySerializer, \
    UserCreateSerializer, FeedbackMessageSerializer, UserFIOSerializer, CreateFeedbackMessageSerializer
from django.contrib.auth import get_user_model
from  .models import Category, Transaction, FeedbackMessage
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseBadRequest
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsStaffOrReadOnly, IsOwnerOrReadOnly
from django.contrib.auth.hashers import make_password, PBKDF2SHA1PasswordHasher

from django.db import models
from rest_framework.decorators import api_view



class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if (self.action == 'list') or (self.action == 'update'):
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


    def create(self, request, *args, **kwargs):
        data = request.data
        print("1")
        data['password'] = make_password(data['password'])
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        if 'password' in data:
            data['password'] = make_password(data['password'])
        # data['password'] = make_password(data['password'])
        serializer = UserCreateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            instance, created = get_user_model().objects.update_or_create(email=serializer.validated_data.get('email', None),
                                                                    defaults=serializer.validated_data)
            if not created:
                serializer.update(instance, serializer.validated_data)
            return Response(request.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        from_user = request.user.pk
        request.data['from_user'] = from_user
        request.data['category'] = 1
        # сделать гет по имени категории
        if serializer.is_valid():
            to_user = request.data['to_user']
            amount = int(request.data['amount'])
            From_User = get_user_model().objects.get(pk=from_user)
            To_User = get_user_model().objects.get(pk=to_user)
            if int(From_User.share_points) < amount:
                return HttpResponseBadRequest({'Недостаточно средств'})
            To_User.personal_points = str(int(To_User.personal_points) + amount)
            From_User.share_points = str(int(From_User.share_points) - amount)
            To_User.save()
            From_User.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    def superpost(request, format=None):
        data = request.data
        data['from_user'] = request.user.pk
        upd_users = data['to_user']


        if data['amount'] not in [10,15,20]:
            return HttpResponseBadRequest({'Not valid amount of points'})

        s_data = []
        for to_user in upd_users:
            data['to_user'] = to_user
            line = data.copy()
            s_data.append(line)

        serializer = TransactionSerializer(data=s_data, many=True)
        if serializer.is_valid():
            users = get_user_model().objects.filter(pk__in=upd_users)
            for to_user in users:
                to_user.personal_points = str(int(to_user.personal_points) + data['amount'])
                to_user.save()
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)




        print(len(users))
        print(category.name)





        # сделать гет по имени категории

        # serializer = TransactionSerializer(data=request.data)
        # if serializer.is_valid():
        #     to_user = request.data['to_user']
        #     amount = int(request.data['amount'])
        #     From_User = get_user_model().objects.get(pk=from_user)
        #     To_User = get_user_model().objects.get(pk=to_user)
        #     if int(From_User.share_points) < amount:
        #         return HttpResponseBadRequest({'Недостаточно средств'})
        #     To_User.personal_points = str(int(To_User.personal_points) + amount)
        #     From_User.share_points = str(int(From_User.share_points) - amount)
        #     To_User.save()
        #     From_User.save()
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedbackMessageViewSet(viewsets.ModelViewSet):
    queryset = FeedbackMessage.objects.all().order_by('created_at').reverse()
    serializer_class = FeedbackMessageSerializer

    def get_permissions(self):
        if (self.action == 'create'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):

        data = request.data
        print(request.user.pk)
        data['author'] = request.user.pk

        # new_fb = form.save()
        # profile = profileform.save(commit=False)
        # if profile.user_id is None:
        #     profile.user_id = new_user.id
        # profile.save()

        serializer = CreateFeedbackMessageSerializer(data=data)
        # serializer.author_id = request.user.pk
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
def job():
    print("I'm working...")
#
# schedule.every(1).seconds.do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(311)