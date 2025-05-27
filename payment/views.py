import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
class AllPage(View):
    def get(self, request):
        try:
            items = Item.objects.all()
            return render(request, 'allPage.html', {'items': items})
        except Exception as e:
            return HttpResponse(e)


class ItemPage(View):
    def get(self, request, id):
        try:
            item = Item.objects.get(id=id)
            return render(request, 'itemPage.html', {'item': item})
        except Exception as e:
            return HttpResponse(e)


class ItemBuy(View):
    def get(self, id):
        try:
            item = Item.objects.get(id=id)

            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel',
            )
            return JsonResponse({'session_id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class OrderBuy(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            item_ids = data.get('order', [])

            if len(item_ids) < 1:
                return JsonResponse({'error': 'order must contain at least 1 item'})

            line_items = []
            order_obj = Order.objects.create()
            for item_id in item_ids:
                try:
                    item_obj = Item.objects.get(id=item_id)
                    OrderItem.objects.create(order=order_obj, item=item_obj)

                    line_items.append({
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': item_obj.name,
                                'description': item_obj.description,
                            },
                            'unit_amount': int(item_obj.price * 100),  # цена в центах
                        },
                        'quantity': 1,
                    })

                except Item.DoesNotExist:
                    continue

            session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel',
            )

            return JsonResponse({'session_id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})
