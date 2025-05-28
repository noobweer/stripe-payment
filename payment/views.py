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
            discounts = Discount.objects.filter(active=True)
            return render(request, 'allPage.html', {'items': items, 'discounts': discounts})
        except Exception as e:
            return HttpResponse(e)


class ItemPage(View):
    def get(self, request, id):
        try:
            item = Item.objects.get(id=id)
            discounts = Discount.objects.filter(active=True)
            return render(request, 'itemPage.html', {'item': item, 'discounts': discounts})
        except Exception as e:
            return HttpResponse(e)


class ItemBuy(View):
    def get(self, request, id):
        try:
            item = Item.objects.get(id=id)
            discount_id = request.GET.get('discount_id')

            if discount_id and Discount.objects.filter(stripe_id=discount_id, active=True).exists():
                discount = {'coupon': Discount.objects.get(stripe_id=discount_id).stripe_id}
            else:
                discount = None

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
                discounts=discount,
            )
            return JsonResponse({'session_id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class OrderBuy(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            item_ids = data.get('order', [])
            discount_id = data.get('discount_id')

            print(data)
            if not item_ids:
                return JsonResponse({'error': 'Order must contain at least one item'}, status=400)

            line_items = []
            discounts = []
            if discount_id and Discount.objects.filter(stripe_id=discount_id, active=True).exists():
                discount_obj = Discount.objects.get(stripe_id=discount_id)
                discounts.append({"coupon": discount_obj.stripe_id})

                order_obj = Order.objects.create(discount=discount_obj)
            else:
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
                            'unit_amount': int(item_obj.price * 100),
                        },
                        'quantity': 1,
                    })

                except Item.DoesNotExist:
                    continue

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel',
                discounts=discounts,
            )

            return JsonResponse({'session_id': session.id})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
