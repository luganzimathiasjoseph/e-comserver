from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from store.models import Profile, Customer
from django.core.exceptions import ObjectDoesNotExist
from store.backends import User
from store.forms import Customer_ProfileForm
from django.db.models import Q
from store.models import *
from django.contrib import messages
import json
from django.http import JsonResponse
from store.cart import Cart


def dashboard(request):
    if 'q' in request.GET:
        q = request.GET['q']
        products = Product.objects.filter(Q(name__icontains=q) | Q(price__icontains=q))
    else:
        products = Product.objects.all()
   
    # Ensure the authenticated user is a Customer
    if request.user.is_authenticated:
        user = request.user
        if hasattr(user, 'customer'):  # Check if user is a Customer
            customer = user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cart_items = order.get_cart_items()
        else:
            cart_items = 0
    else:
        cart_items = 0

    context = {
        "products": products,
        'cartItems': cart_items
    }
    return render(request, "customer/dashboard.html", context)

def search_items(request):
    # If the user has searched for a product
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query).order_by("created_at") 
    context ={
        "products": products,
        "query":query,
    }
    return render(request, 'customer/search_items.html', context)
    


def category(request,pa):
    # Replace hyphen with the space when searching
    pa = pa.replace('-', ' ')
    # grab the category from the url
    try:
        category = Category.objects.get(name=pa)
        products = Product.objects.filter(category=category)
        return render(request,'customer/category.html',{'category': category, "products":products})
        
    except:
        messages.success(request,("that Category Doesn't Exist"))
        return redirect('customer:dashboard')


@login_required
def checkout(request):
    cart =Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.totals()
    customers=Customer.objects.all()
    
    return render(request, 'customer/checkout.html', {'cart_products':cart_products,'quantities':quantities,'totals':totals,'customers':customers})
   

@login_required
def product(request, pk):
    user = request.user
    if hasattr(user, 'customer'):  # Check if user is a Customer
        customer = user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
        
    product = Product.objects.get(id=pk)
    context = {
        "product": product,
        'cartItems': cartItems
    }
    return render(request, "customer/product.html", context)

@login_required
def cart_summary(request):
    cart =Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.totals()
    
    
    return render(request, 'customer/cart_summary.html', {'cart_products':cart_products,'quantities':quantities,'totals':totals})


@login_required
def profile(request):
    profile = None
    try:
        profile = request.user.profile
        form = Customer_ProfileForm(instance=profile)
    except ObjectDoesNotExist:
        profile = None
        form = Customer_ProfileForm()

    if request.method == 'POST':
        form = Customer_ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('staff:account')

    return render(request, 'customer/Profile.html', {'form': form, 'profile': profile})

def cart_add(request):
    cart =Cart(request)
    # test for post
    if request.POST.get('action') =='post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty =int(request.POST.get('product_qty'))
        # look up product in the database
        product = get_object_or_404(Product, id=product_id)
        # save to session
        cart.add(product=product,quantity = product_qty)
        # Get cart quantity
        cart_quantity = cart.__len__()
        
        # return a response 
        response = JsonResponse({'qty' : cart_quantity})
        return response
        
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        try:
            productid = int(request.POST.get('productid'))
            product_qty = int(request.POST.get('product_qty'))
        except ValueError:
            return JsonResponse({'error': 'Invalid product ID or quantity'})

        cart.update(product=productid, quantity=product_qty)
        return JsonResponse({'qty': product_qty})
    else:
        return JsonResponse({'error': 'Invalid action'})
 
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get product ID
        product_id = int(request.POST.get('product_id'))  # Corrected variable name
        
        # Call delete function    
        cart.delete(product_id)  # Corrected function call
        response = JsonResponse({'product': product_id})
        return response
    
def languages(request):
    return render(request, 'customer/languages.html')
