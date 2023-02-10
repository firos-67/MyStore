from django.contrib.auth.models import User

from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.core.exceptions import ObjectDoesNotExist


def counter(request):
    cart_count = 0
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        user = None
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart, active=True)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
