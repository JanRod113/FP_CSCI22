from django.shortcuts import render, get_object_or_404, redirect
from .models import Food, Order, OrderItem, Customer
from .forms import FoodForm, OrderForm, OrderItemForm
from django.forms import inlineformset_factory

# Food views
def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_food')
    else:
        form = FoodForm()
    return render(request, 'add_food.html', {'form': form})

def food_detail(request, pk):
    food = get_object_or_404(Food, pk=pk)
    return render(request, 'food_detail.html', {'food': food})

def edit_food(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect('food_detail', pk=food.pk)
    else:
        form = FoodForm(instance=food)
    return render(request, 'edit_food.html', {'form': form})

def delete_food(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'POST':
        food.delete()
        return redirect('list_food')
    return render(request, 'delete_food.html', {'food': food})

def list_food(request):
    foods = Food.objects.all()
    return render(request, 'list_food.html', {'foods': foods})

# Order views
OrderItemFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

def add_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_item_forms = OrderItemFormset(request.POST)
        if order_form.is_valid() and order_item_forms.is_valid():
            order = order_form.save()
            order_item_forms.instance = order
            order_item_forms.save()
            return redirect('list_orders')
    else:
        order_form = OrderForm()
        order_item_forms = OrderItemFormset()
    return render(request, 'add_order.html', {
        'order_form': order_form,
        'order_item_forms': order_item_forms
    })

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    total_price = sum(item.quantity * item.food.price for item in order_items)
    return render(request, 'order_detail.html', {
        'order': order,
        'order_items': order_items,
        'total_price': total_price
    })

def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)
        order_item_forms = OrderItemFormset(request.POST, instance=order)
        if order_form.is_valid() and order_item_forms.is_valid():
            order = order_form.save()
            order_item_forms.save()
            return redirect('order_detail', pk=order.pk)
    else:
        order_form = OrderForm(instance=order)
        order_item_forms = OrderItemFormset(instance=order)
    return render(request, 'edit_order.html', {
        'order_form': order_form,
        'order_item_forms': order_item_forms
    })

def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('list_orders')
    return render(request, 'delete_order.html', {'order': order})

def list_orders(request):
    orders = Order.objects.all()
    return render(request, 'list_orders.html', {'orders': orders})

# Customer views (Assuming a Customer detail view exists)
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    orders = Order.objects.filter(customer=customer)
    return render(request, 'customer_detail.html', {'customer': customer, 'orders': orders})
