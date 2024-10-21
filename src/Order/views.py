from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Item, OrderItems, Order
# Create your views here.

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home_page.html"

class ProductDetailView(DetailView):
    model = Item
    template_name = "product.html"

def add_to_cart(request, slug):
    # Fetch the item using the provided slug, 404 if not found
    item = get_object_or_404(Item, slug=slug)
    
    # Query for an active order for the current user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    # Check if an active order exists
    if order_qs.exists():
        # Get the first order from the queryset
        order = order_qs[0]
        
        # Check if the item is already in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = order.items.get(item__slug=item.slug)
            order_item.quantity += 1
            order_item.save()
        else:
            order_item = OrderItems.objects.create(user=request.user, item=item)
            order.items.add(order_item)
    else:
        # Adds an ordered date for the order
        ordered_date = timezone.now()
        
        # If no active order, create a new order
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date,
        )
        
        # Add the new order item to the order
        order_item = OrderItems.objects.create(user=request.user, item=item)
        order.items.add(order_item)
    
    # Correct redirect
    return redirect('product', slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user = request.user,
        ordered=False
    )

    # Check if an active order exists
    if order_qs.exists():
        order = order_qs[0]
        # Check if the item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItems.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]

            order.items.remove(order_item)
            order_item.delete()
        else:
            # Add a message saying the order doesn't contain the item
            messages.info(request, "This item was not in your cart")
    else:
        # Add a message saying the user doesn't have an order
        messages.info(request, "You do not have an active order")

    return redirect("product", slug=slug)


def checkout(request):
    return render(request, 'checkout_page.html')


