from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Products
from cart.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.info(request,"Please Login to add items to your cart")
        return redirect('credentials:login')
    product = Products.objects.get(id=product_id)
    user = User.objects.get(username=request.user)
    try:
        # cart = Cart.objects.get(cart_id=_cart_id(request))
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request),user=user)
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except ObjectDoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()
    return redirect('cart:cart_details')


@login_required(login_url='credentials:login')
def cart_details(request, total=0, counter=0, cart_items=None):
    user = User.objects.get(username=request.user)
    print(user)
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))


@login_required(login_url='credentials:login')
def cart_minus(request, product_id):
    user = User.objects.get(username=request.user)
    cart = Cart.objects.get(user=user)
    product = Products.objects.get(id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart.delete()
    return redirect('cart:cart_details')


@login_required(login_url='credentials:login')
def cart_remove(request, product_id):
    user = User.objects.get(username=request.user)
    cart=Cart.objects.get(user=user)
    product = get_object_or_404(Products,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart:cart_details')
