from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, F
from django.http import JsonResponse
from inventory.models import Product, Category, Supplier, Order
from django.utils import timezone
from datetime import timedelta

@login_required(login_url='login')
def dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()
    total_orders = Order.objects.count()
    low_stock_count = Product.objects.filter(quantity__lte=F('low_stock_threshold')).count()

    recent_orders = Order.objects.all()[:5]

    low_stock_products = Product.objects.filter(
        quantity__lte=F('low_stock_threshold')
    ).order_by('quantity')[:5]

    top_products = Product.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')[:5]

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'total_orders': total_orders,
        'low_stock_count': low_stock_count,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'top_products': top_products,
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='login')
def chart_data(request):
    chart_type = request.GET.get('type', 'orders_per_month')

    if chart_type == 'orders_per_month':
        data = get_orders_per_month()
    else:
        data = {}

    return JsonResponse(data)


def get_orders_per_month():
    months = []
    labels = []

    for i in range(11, -1, -1):
        date = timezone.now() - timedelta(days=30 * i)
        month_year = date.strftime('%B %Y')
        labels.append(month_year)

        start = date.replace(day=1)
        if i == 0:
            end = timezone.now()
        else:
            end = (date.replace(day=1) + timedelta(days=32)).replace(day=1)

        count = Order.objects.filter(
            created_at__gte=start,
            created_at__lt=end
        ).count()
        months.append(count)

    return {
        'labels': labels,
        'datasets': [{
            'label': 'Orders',
            'data': months,
            'borderColor': '#17a2b8',
            'backgroundColor': 'rgba(23, 162, 184, 0.1)',
            'borderWidth': 2,
        }]
    }