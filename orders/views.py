from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from inventory.models import Order, OrderItem, Product

@login_required(login_url='login')
def order_list(request):
    if request.user.profile.is_admin():
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required(login_url='login')
def order_create(request):
    if request.method == 'POST':
        try:
            order = Order.objects.create(user=request.user)

            product_ids = request.POST.getlist('product_id')
            quantities = request.POST.getlist('quantity')

            if not product_ids:
                messages.error(request, 'Please select at least one product.')
                order.delete()
                return redirect('order_create')

            total_amount = 0

            for product_id, quantity in zip(product_ids, quantities):
                if not product_id or not quantity or int(quantity) <= 0:
                    continue

                product = get_object_or_404(Product, pk=product_id)
                quantity = int(quantity)

                if product.quantity < quantity:
                    messages.error(
                        request,
                        f'Insufficient stock for {product.name}. Available: {product.quantity}'
                    )
                    order.delete()
                    return redirect('order_create')

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price_at_order=product.price
                )

                product.quantity -= quantity
                product.save()

                total_amount += quantity * product.price

                if product.is_low_stock():
                    send_low_stock_alert(product)

            order.total_amount = total_amount
            order.status = 'completed'
            order.save()

            messages.success(request, f'Order #{order.order_number} created successfully.')
            return redirect('order_detail', pk=order.pk)

        except Exception as e:
            messages.error(request, f'Error creating order: {str(e)}')
            return redirect('order_create')

    products = Product.objects.filter(quantity__gt=0)
    return render(request, 'orders/order_form.html', {'products': products})


@login_required(login_url='login')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if not request.user.profile.is_admin() and order.user != request.user:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('order_list')

    items = order.items.all()

    return render(request, 'orders/order_detail.html', {'order': order, 'items': items})


def send_low_stock_alert(product):
    try:
        from django.core.mail import send_mail
        from django.conf import settings

        subject = f'Low Stock Alert: {product.name}'
        message = f"""
        Product: {product.name} (SKU: {product.sku})
        Current Stock: {product.quantity}
        Threshold: {product.low_stock_threshold}

        Please reorder this product.
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['admin@inventory-system.com'],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending email: {str(e)}")