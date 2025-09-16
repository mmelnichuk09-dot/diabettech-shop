from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_order(request):
    # просто рендерим главную страницу
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'shop_orders/index.html', context)


@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            full_name = data.get('fullName')
            postal_code = data.get('postalCode')
            address = data.get('address')
            phone = data.get('phone')
            email = data.get('email')
            quantity = int(data.get('quantity', 1))

            # Считаем сумму на сервере
            amount = 1 * quantity * 100  # в центах

            # Создаем PaymentIntent напрямую без модели
            token = data.get('token')
            payment_method = stripe.PaymentMethod.create(
                type='card',
                card={'token': token}
            )
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='eur',
                payment_method_types=['card'],
                payment_method=payment_method.id
            )
            stripe.PaymentIntent.confirm(intent.id)

            # Отправляем email клиенту и себе
            send_mail(
                'Order Confirmation',
                f"Thank you for your order!\n\n"
                f"Name: {full_name}\n"
                f"Postal Code: {postal_code}\n"
                f"Address: {address}\n"
                f"Phone: {phone}\n"
                f"Email: {email}\n"
                f"Quantity: {quantity}\n"
                f"Total: €{69 * quantity}\n"
                f"Delivery: Free (4-7 days)\n"
                f"Once order is shipped, we’ll send you a tracking number",
                settings.EMAIL_HOST_USER,
                [email, settings.EMAIL_HOST_USER],
                fail_silently=False
            )

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Only POST allowed'})


def order_success(request):
    return render(request, 'shop_orders/order_success.html')
