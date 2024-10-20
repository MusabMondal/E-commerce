from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Item, OrderItems, Order
# Create your views here.

class HomeView(ListView):
    model = Item
    template_name = "home_page.html"

class ProductDetailView(DetailView):
    model = Item
    template_name = "product.html"

def add_to_cart(request, slug):
    # Fetch the item using the provided slug, 404 if not found
    item = get_object_or_404(Item, slug=slug)

    # Create a new OrderItem for the item
    order_item = OrderItems.objects.get_or_create(
        item=item,
        user = request.user,
        ordered=False
        )

    # Query for an active order for the current user
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    # Check if an active order exists
    if order_qs.exists():
        # Get the first order from the queryset
        order = order_qs[0]
        
        # Check if the item is already in the order
        if order.items.filter(item__slug=item.slug).exists():
            # If it is, increment the quantity of the order item
            order_item.quantity += 1
            order_item.save()
        else:
            # If it isn't, add the order item to the order
            order.items.add(order_item)
    else:
        #Adds a ordered date for the order
        ordered_date = timezone.now()
        # If no active order, create a new order
        order = Order.objects.create(
            user=request.user,
            ordered_date = ordered_date,
            )
        
        # Add the new order item to the order
        order.items.add(order_item)

    return redirect("product", slug=slug)


def checkout(request):
    return render(request, 'checkout_page.html')


