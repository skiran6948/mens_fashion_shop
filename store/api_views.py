from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product, Category, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from cart.cart import Cart
from store.models import Product

# Products & Categories: ViewSets (list, retrieve)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    lookup_field = 'slug'        # allow /api/products/<slug>/
    lookup_value_regex = '[^/]+' # allow hyphens, etc.

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

# Products by category
@api_view(['GET'])
def category_products_api(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=cat)
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response({'category': CategorySerializer(cat, context={'request':request}).data, 'products': serializer.data})

# Orders: list/create
class OrderCreateListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        # if user authenticated show their orders, else empty
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(user=user).order_by('-date')
        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.context['request'] = self.request
        serializer.save()

# Admin: orders list (requires staff)
class AdminOrderList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('-date')

# Simple register endpoint
@api_view(['POST'])
def register_api(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error':'username and password required'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error':'username exists'}, status=400)
    user = User.objects.create_user(username=username, email=email, password=password)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=201)

# Token logout (blacklist refresh token) optional
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_api(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'detail':'Logged out'}, status=205)
    except Exception:
        return Response(status=400)


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
    return Response({'items': items, 'total': cart.get_total_price()})


@api_view(['POST'])
def api_cart_add(request):
    pid = request.data.get('product_id')
    qty = int(request.data.get('quantity', 1))
    product = get_object_or_404(Product, id=pid)
    cart = Cart(request)
    cart.add(product=product, quantity=qty)
    return Response({'detail':'added'})


@api_view(['POST'])
def api_cart_remove(request):
    pid = request.data.get('product_id')
    product = get_object_or_404(Product, id=pid)
    cart = Cart(request)
    cart.remove(product)
    return Response({'detail':'removed'})


@api_view(['GET'])
def search_api(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response({'results': serializer.data})

@api_view(['GET'])
def search_suggestions_api(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)[:5]
    data = [{'name': p.name, 'slug': p.slug} for p in products]
    return Response(data)


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
    return Response({'items': items, 'total': cart.get_total_price()})



@api_view(['POST'])
def api_cart_add(request):
    pid = request.data.get('product_id')
    qty = int(request.data.get('quantity', 1))
    product = get_object_or_404(Product, id=pid)
    Cart(request).add(product=product, quantity=qty)
    return Response({'detail': 'Product added'})


@api_view(['POST'])
def api_cart_remove(request):
    pid = request.data.get('product_id')
    product = get_object_or_404(Product, id=pid)
    Cart(request).remove(product)
    return Response({'detail': 'Product removed'})



class OrderListCreateAPI(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)