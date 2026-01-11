# orders/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Order, OrderItem
from cart.models import CartItem
from cart.views import _get_session_key  # for guests


def order_history(request):
    if request.user.is_authenticated:
        orders = (
            Order.objects
            .prefetch_related('items')
            .filter(user=request.user)
            .order_by('-placed_at')
        )
    else:
        session_key = _get_session_key(request)
        orders = (
            Order.objects
            .prefetch_related('items')
            .filter(session_key=session_key)
            .order_by('-placed_at')
        )

    return render(request, 'orders/history.html', {'orders': orders})


def simulate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.is_paid = True
        order.save()
        return redirect('orders:history')

    return render(request, 'orders/payment_fake.html', {'order': order})


# ✅ NEW: place_order view to save user/session_key in Order
def place_order(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        order = Order.objects.create(user=request.user, is_paid=False)
    else:
        session_key = _get_session_key(request)
        cart_items = CartItem.objects.filter(session_key=session_key)
        order = Order.objects.create(session_key=session_key, is_paid=False)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            item=item.item,
            quantity=item.quantity
        )
    cart_items.delete()

    return redirect('orders:simulate_payment', order_id=order.id)
