from django.urls import path

from .views import (HomeView, 
                    checkout,
                    ProductDetailView,
                    add_to_cart
                    )

urlpatterns = [
    # Add your URL patterns here
    path('', HomeView.as_view(), name='home_page'),
    path('checkout/', checkout, name='checkout'),
    path('product/<slug:slug>/',ProductDetailView.as_view(), name='product'),
    path('add_to_cart/<slug:slug>/', add_to_cart, name='add_to_cart')
]
