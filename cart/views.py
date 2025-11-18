from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from main.models import Product, Order, OrderItem
from .cart import Cart
from .forms import *

# Create your views here.

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', context={'cart':cart})

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_clear(request):
    cart=Cart(request)
    cart.clear()
    return redirect('cart_detail')

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.add(
            product=product,
            count=form.cleaned_data['count'],
            update_count=form.cleaned_data['count']
        )
    return redirect('cart_detail')

@login_required
def cart_buy(request):
    cart = Cart(request)
    if cart.__len__()<=0:
        return redirect('list_product_filter')
    form = OrderForm(request.POST)
    if form.is_valid():
        order = Order.objects.create(
            buyer_firstname=form.cleaned_data['buyer_firstname'],
            buyer_surname=form.cleaned_data['buyer_surname'],
            comment=form.cleaned_data['comment'],
            delivery_address=form.cleaned_data['delivery_address'],
            total_price=cart.get_total_price(),
            user=request.user
        )
        order.price = cart.get_total_price()
        for item in cart:
            order_item=OrderItem.objects.create(
                product=item['product'],
                quantity=item['count'],
                order=order,
            )
        cart.clear()
    return redirect('cart_detail')

@login_required
def open_order(request):
    context={
        'form_order': OrderForm
    }
    return render(request, 'order/order_form.html', context)