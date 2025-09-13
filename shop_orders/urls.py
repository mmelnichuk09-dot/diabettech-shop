from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_order, name='create_order'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('order-success/', views.order_success, name='order_success'),
]