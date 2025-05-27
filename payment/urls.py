from django.urls import path
from .views import *

urlpatterns = [
    path('', AllPage.as_view(), name='all-page'),
    path('item/<int:id>/', ItemPage.as_view(), name='item-page'),
    path('buy/<int:id>/', ItemBuy.as_view(), name='item-buy'),
    path('order/', OrderBuy.as_view(), name='order-buy'),
]