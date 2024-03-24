from django.shortcuts import render,redirect,get_object_or_404
from .models import *
# Create your views here.
def store(request):
    products = Product.objects.all()
    # print(products)
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items,'order':order}
    return render(request,  'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items,'order':order}
    return render(request,  'store/checkout.html', context)

def add_to_cart(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=id)
        user = request.user
        # Filter to find existing AddCart objects for the user and product
        cart_items = AddCart.objects.filter(user=user, product=product)
        if cart_items.exists():
            # If cart items exist, increment the quantity of the first one found
            cart_item = cart_items.first()
            cart_item.quantity += 1
            cart_item.save()  # Save the cart item after updating the quantity
        else:
            # If no cart items exist, create a new one
            AddCart.objects.create(user=user, product=product)
        return redirect('cart')
    else:
        return redirect('cart')
    
def view_cart(request):
    print("Viewing cart...")
    if request.user.is_authenticated:
        # Fetch the cart items associated with the current user
        cart_items = AddCart.objects.filter(user=request.user)
        context = {'cart_items': cart_items}
        return render(request, 'store/cart.html', context)
    else:
        return redirect('cart')