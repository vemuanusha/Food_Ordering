from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from menu.models import MenuItem
from .models import CartItem
from orders.models import Order, OrderItem


def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
    else:
        cart_item, created = CartItem.objects.get_or_create(
            session_key=_get_session_key(request), item=item
        )

    cart_item.quantity += 1
    cart_item.save()

    if created:
        messages.success(request, f' “{item.name}” added to cart!')
    else:
        messages.info(request, f'Quantity increased for “{item.name}”.')

    return redirect('cart:view')


def view_cart(request):
    items = (CartItem.objects.filter(user=request.user)
             if request.user.is_authenticated
             else CartItem.objects.filter(session_key=_get_session_key(request)))
    total = sum(ci.line_total() for ci in items)
    return render(request, 'cart/cart.html', {'items': items, 'total': total})


def change_quantity(request, item_id, delta):
    delta = int(delta)
    try:
        ci = (CartItem.objects.get(user=request.user, item_id=item_id)
              if request.user.is_authenticated
              else CartItem.objects.get(session_key=_get_session_key(request), item_id=item_id))

        ci.quantity += delta
        if ci.quantity <= 0:
            ci.delete()
            messages.error(request, '🗑️ Item removed from cart.')
        else:
            ci.save()
            messages.success(request, 'Cart updated.')
    except CartItem.DoesNotExist:
        pass
    return redirect('cart:view')


def remove_from_cart(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    qs = (CartItem.objects.filter(user=request.user, item_id=item_id)
          if request.user.is_authenticated
          else CartItem.objects.filter(session_key=_get_session_key(request), item_id=item_id))
    qs.delete()
    messages.error(request, f'🗑️ “{item.name}” removed from cart.')
    return redirect('cart:view')


def place_order(request):
    cart_items = (
        CartItem.objects.filter(user=request.user)
        if request.user.is_authenticated
        else CartItem.objects.filter(session_key=_get_session_key(request))
    )

    if not cart_items.exists():
        messages.info(request, '🛒 Cart is empty.')
        return redirect('cart:view')

    if request.user.is_authenticated:
        order = Order.objects.create(
            user=request.user,
            is_paid=False,
            placed_at=timezone.now()
        )
    else:
        session_key = _get_session_key(request)
        order = Order.objects.create(
            session_key=session_key,
            is_paid=False,
            placed_at=timezone.now()
        )

    for ci in cart_items:
        OrderItem.objects.create(order=order, item=ci.item, quantity=ci.quantity)

    cart_items.delete()
    messages.success(request, f'✅ Order #{order.id} placed and saved in history!')

    # ✅ Redirect to payment AFTER saving — history can now display it
    return redirect('orders:simulate_payment', order_id=order.id)