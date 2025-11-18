from django.urls import path
from .views import *

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('clear/', cart_clear, name='cart_clear'),
    path('buy/', cart_buy, name='cart_buy'),
    path('create_order/', open_order, name='order_open'),
]
