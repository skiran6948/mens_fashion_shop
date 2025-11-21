from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from cart.cart import Cart
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def api_cart_detail(request):
    cart = Cart(request)
    items = []

    for item in cart:
        items.append({
            'product_id': item['product'].id,
            'name': item['product'].name,
            'price': item['price'],
            'quantity': item['quantity']
        })
    
    return Response({
        'items': items,
        'total': cart.get_total_price()
    })


@api_view(['POST'])
def api_cart_add(request):
    pid = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))

    product = get_object_or_404(Product, id=pid)

    cart = Cart(request)
    cart.add(product=product, quantity=quantity)

    return Response({'detail': 'Product added to cart'})


@api_view(['POST'])
def api_cart_remove(request):
    pid = request.data.get('product_id')
    product = get_object_or_404(Product, id=pid)

    cart = Cart(request)
    cart.remove(product)

    return Response({'detail': 'Product removed'})
