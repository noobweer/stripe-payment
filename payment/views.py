from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from .models import *
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
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

