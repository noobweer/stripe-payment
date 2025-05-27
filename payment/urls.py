from django.urls import path
from .views import *

urlpatterns = [
    path('item/<int:id>/', ItemPage.as_view(), name='item-page'),
    path('buy/<int:id>/', ItemBuy.as_view(), name='item-buy'),
]