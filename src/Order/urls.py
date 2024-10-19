from django.urls import path

from .views import HomeView, checkout, ProductDetailView

urlpatterns = [
    # Add your URL patterns here
    path('', HomeView.as_view(), name='home_page'),
    path('checkout/', checkout, name='checkout'),
    path('product/<slug>/',ProductDetailView.as_view(), name='product')
]
