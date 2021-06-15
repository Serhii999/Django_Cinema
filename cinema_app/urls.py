from django.urls import path, re_path
from cinema_app.views import *


urlpatterns = [
    path('', HallsListView.as_view(), name='main'),
    path('login/', Login.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('hall/create/', HallCreateView.as_view(), name='hall_create'),
    path('session/create/<int:pk>', SessionCreateView.as_view(), name='session_create'),
    path('today/', TodaySessionView.as_view(), name='today_sessions'),
    path('purchase/ticket/', PurchaseTicketView.as_view(), name='purchase'),
    path('my_purchases', Purchases.as_view(), name='my_purchases'),
    path('hall_update/<int:pk>', UpdateHallView.as_view(), name='hall_update'),
    path('session_update/<int:pk>', UpdateSessionView.as_view(), name='session_update')
    ]