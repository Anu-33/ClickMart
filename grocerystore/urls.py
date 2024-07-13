from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ItemListView, ItemDetailView, register, add_to_cart, cart_view

urlpatterns = [
    path('', ItemListView.as_view(), name='store-home'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('cart/', cart_view, name='cart-view'),
    path('item/<int:pk>/add_to_cart/', add_to_cart, name='add-to-cart'),
]
