from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .cart import Cart
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from store.models import Order, OrderItem


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def decrease_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrease(product)
    return redirect('cart_detail')

def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        total = cart.get_total_price()

        # ✅ Create the order
        order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        name=name,
        email=email,
        phone=phone,
        address=address,
        total_price=total
    )

        # ✅ Create order items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        # ✅ Clear cart after saving order
        cart.clear()

        return render(request, 'cart/checkout_success.html', {
            'name': name,
            'order': order
        })

    return render(request, 'cart/checkout.html', {'cart': cart})
