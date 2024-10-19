from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Item
# Create your views here.

class HomeView(ListView):
    model = Item
    template_name = "home_page.html"

class ProductDetailView(DetailView):
    model = Item
    template_name = "product.html"

def display_items(request):
    items = Item.objects.all()
    return render(request, 'home_page.html', {'items': items})

def checkout(request):
    return render(request, 'checkout_page.html')

def product(request):
    return render(request, 'product.html')