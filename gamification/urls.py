from django.conf.urls import include, url
from gamification.views import UserViewSet, TransactionsViewSet, CategoryViewSet, FeedbackMessageViewSet, ExcelHandler\
    ,ProductViewSet, OrderViewSet, start

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Создаем router и регистрируем наш ViewSet
router = routers.DefaultRouter()
router.register(r'users', viewset=UserViewSet)
router.register(r'categories', viewset=CategoryViewSet)
router.register(r'feedbackmessages', viewset=FeedbackMessageViewSet)
router.register(r'products', viewset=ProductViewSet)
router.register(r'orders', viewset=OrderViewSet)

urlpatterns =[
    url(r'^', include(router.urls)),
    url(r'^auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^transactions/', TransactionsViewSet.as_view({'post':'post', 'get':'list' } ), name='add transaction'),
    url(r'^supertransactions/', TransactionsViewSet.superpost, name='superpost'),
    url(r'^sharepoints/', UserViewSet.month_update, name='month_upd'),
    url(r'^excel/', ExcelHandler.as_view({'post':'export_xls'}), name='excel_gen'),
    # url(r'^interests/', UserViewSet.as_view({'post':'add_interest', 'get':'get_interest'})),


    # url(r'^auth/datatoken/', MyTokenObtainPairView.as_view(), name='datatoken_obtain_pair_and_user'),
]