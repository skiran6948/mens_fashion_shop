import json
from datetime import timedelta
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.shortcuts import render
from django.urls import path
from django.contrib.admin import AdminSite
from .models import Product, Category, Order, OrderItem

class CustomAdminSite(AdminSite):
    site_header = "Men's Fashion Store Admin"
    site_title = "Men's Fashion Admin"
    index_title = "Dashboard Overview"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        from .models import Order, OrderItem

        # date range filter
        range_filter = request.GET.get('range', 'all')
        today = timezone.now().date()

        if range_filter == 'today':
            start_date = today
        elif range_filter == 'week':
            start_date = today - timedelta(days=7)
        elif range_filter == 'month':
            start_date = today - timedelta(days=30)
        else:
            start_date = None

        orders = Order.objects.all()
        if start_date:
            orders = orders.filter(date__date__gte=start_date)

        total_orders = orders.count()
        total_revenue = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
        total_customers = orders.values('email').distinct().count()

        # order status count
        status_counts = (
            orders.values('status')
            .annotate(count=Count('status'))
            .order_by('status')
        )

        # revenue trend
        revenue_trend = (
            orders.annotate(date_only=TruncDate('date'))
            .values('date_only')
            .annotate(total=Sum('total_price'))
            .order_by('date_only')
        )

        labels = [item['date_only'].strftime('%Y-%m-%d') for item in revenue_trend if item['date_only']]
        totals = [float(item['total']) for item in revenue_trend]

        # top products
        top_products = (
            OrderItem.objects.values('product__name')
            .annotate(total_sold=Sum('quantity'))
            .order_by('-total_sold')[:5]
        )

        context = {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_customers': total_customers,
            'status_counts': status_counts,
            'top_products': top_products,
            'range_filter': range_filter,
            'labels': json.dumps(labels),
            'totals': json.dumps(totals),
        }
        return render(request, 'admin/dashboard.html', context)
    

custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(Product)
custom_admin_site.register(Category)
custom_admin_site.register(Order)
custom_admin_site.register(OrderItem)