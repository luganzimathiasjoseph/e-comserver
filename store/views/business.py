from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from ..models import Profile
from django.core.exceptions import ObjectDoesNotExist
from store.backends import User
from ..forms import ProfileForm
from store.models import *
from store.forms import *
 

@login_required
def profile(request):
    profile = None
    try:
        profile = request.user.profile
        form = ProfileForm(instance=profile)
    except ObjectDoesNotExist:
        profile = None
        form = ProfileForm()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('staff:account')

    return render(request, 'business/Profile.html', {'form': form, 'profile': profile})

@login_required
# @admin_only
def dashboard(request):
    products = Product.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    total_products = products.count()
    total_customers = customers.count()
    
    
    context = {'products':products,'customers':customers,'total_products':total_products,'total_customers':total_customers,'total_orders':total_orders}
    templates = loader.get_template('business/dashboard.html')
    return render(request,'business/dashboard.html',context)



@login_required
# @admin_only
def businesscustomer(request,pk):
    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all()
    templates = loader.get_template('business/businesscustomer.html')
    context ={
        'customer':customer,
        'orders':orders
    }
    return render(request, 'business/businesscustomer.html',context)


def upload(request):
    if request.POST:
        forms = UploadForm(request.POST, request.FILES)
        print(request.FILES)
        if forms.is_valid():
            forms.save()
        return redirect('business:dashboard')
    return render(request, 'business/upload.html',{'form': UploadForm})

def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = UploadForm(instance=product)
    if request.POST:
        forms = UploadForm(request.POST, instance=product)
        
        if forms.is_valid():
            forms.save()
        return redirect('business:dashboard')
    context = {'form': form}
    return render(request, 'business/upload.html',context)

def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method =='POST':
        product.delete()
        return redirect('business:dashboard')
    context ={'product':product}
    return render(request, 'business/delete.html',context)