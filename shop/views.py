from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Category, Order, OrderItem
import json

def index(request):
    """Homepage showing all products"""
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context)

def product_detail(request, product_id):
    """Single product page"""
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

def checkout(request):
    """Checkout page"""
    if request.method == 'POST':
        # Get cart data from session
        cart = request.session.get('cart', {})
        
        # Create order
        order = Order.objects.create(
            customer_name=request.POST['name'],
            customer_phone=request.POST['phone'],
            customer_email=request.POST['email'],
            delivery_address=request.POST['address'],
            total_amount=request.POST['total']
        )
        
        # Create order items
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
        
        # Clear cart
        request.session['cart'] = {}
        
        return redirect('order_success', order_id=order.id)
    
    return render(request, 'shop/checkout.html')

def order_success(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})