from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Item, Cart, Order
from .forms import UserRegisterForm, CartForm, OrderForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('store-home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.item.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart_items:
                order.items.add(item)
            cart_items.delete()
            return redirect('store-home')
    else:
        form = OrderForm()
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'form': form,
        'total_amount': total_amount
    })


class ItemListView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'

class ItemDetailView(DetailView):
    model = Item

@login_required
def add_to_cart(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.user = request.user
            cart_item.item = item
            cart_item.save()
            return redirect('cart-view')
    else:
        form = CartForm()
    return render(request, 'item_detail.html', {'item': item, 'form': form})
