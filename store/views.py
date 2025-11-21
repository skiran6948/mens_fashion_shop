from django.shortcuts import render, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import Order
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category


def home(request):
    products = Product.objects.all()[:4]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories
    })

def shop(request):
    products = Product.objects.all()  # show all products
    return render(request, 'store/shop.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'store/my_orders.html', {'orders': orders})


def search_products(request):
    query = request.GET.get('q', '')      # search keyword
    category = request.GET.get('category')  # get selected category

    # base search: search name + description
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )

    # filter by category if selected
    if category:
        products = products.filter(category__id=category)

    return render(request, 'store/search_results.html', {
        'query': query,
        'products': products
    })


def search_suggestions(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)[:5]

    suggestions = [{'name': p.name, 'slug': p.slug} for p in products]

    return JsonResponse(suggestions, safe=False)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category_products.html', {
        'category': category,
        'products': products
    })
