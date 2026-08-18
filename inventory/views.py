from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .models import Product, Category, Supplier

@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(category__name__icontains=query)
        )

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    stock_status = request.GET.get('stock_status')
    if stock_status == 'low':
        products = [p for p in products if p.is_low_stock()]
    elif stock_status == 'out':
        products = [p for p in products if p.quantity == 0]

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    }
    return render(request, 'inventory/product_list.html', context)


@login_required(login_url='login')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'inventory/product_detail.html', {'product': product})


@login_required(login_url='login')
def product_create(request):
    if not request.user.profile.is_admin():
        messages.error(request, 'You do not have permission to create products.')
        return redirect('product_list')

    if request.method == 'POST':
        try:
            product = Product.objects.create(
                name=request.POST.get('name'),
                sku=request.POST.get('sku'),
                category_id=request.POST.get('category'),
                supplier_id=request.POST.get('supplier'),
                price=request.POST.get('price'),
                quantity=request.POST.get('quantity'),
                low_stock_threshold=request.POST.get('threshold'),
                description=request.POST.get('description')
            )
            messages.success(request, f'Product "{product.name}" created successfully.')
            return redirect('product_detail', pk=product.pk)
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')

    context = {
        'categories': Category.objects.all(),
        'suppliers': Supplier.objects.all(),
    }
    return render(request, 'inventory/product_form.html', context)


@login_required(login_url='login')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if not request.user.profile.is_admin():
        messages.error(request, 'You do not have permission to edit products.')
        return redirect('product_list')

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.sku = request.POST.get('sku')
        product.category_id = request.POST.get('category')
        product.supplier_id = request.POST.get('supplier')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.low_stock_threshold = request.POST.get('threshold')
        product.description = request.POST.get('description')

        try:
            product.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_detail', pk=product.pk)
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')

    context = {
        'product': product,
        'categories': Category.objects.all(),
        'suppliers': Supplier.objects.all(),
        'is_edit': True,
    }
    return render(request, 'inventory/product_form.html', context)


@login_required(login_url='login')
@require_POST
def product_delete(request, pk):
    if not request.user.profile.is_admin():
        messages.error(request, 'You do not have permission to delete products.')
        return redirect('product_list')

    product = get_object_or_404(Product, pk=pk)
    product_name = product.name
    product.delete()
    messages.success(request, f'Product "{product_name}" deleted successfully.')
    return redirect('product_list')


@login_required(login_url='login')
def category_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    return render(request, 'inventory/category_list.html', {'categories': categories})


@login_required(login_url='login')
def supplier_list(request):
    suppliers = Supplier.objects.all()
    paginator = Paginator(suppliers, 10)
    page_number = request.GET.get('page')
    suppliers = paginator.get_page(page_number)
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})


@login_required(login_url='login')
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    products = supplier.products.all()
    return render(request, 'inventory/supplier_detail.html', {'supplier': supplier, 'products': products})