from pyexpat.errors import messages
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import auth
from whitenoise.storage import CompressedStaticFilesStorage
from ..models import Profile
from django.core.exceptions import ObjectDoesNotExist
from store.backends import User
from ..forms import RegistrationForm, ProfileForm
from ..forms import ContactForm

# from django.shortcuts import render_to_response
from django.template import RequestContext



def paymentoptions(request):
    template= loader.get_template('staff/paymentoptions.html')
    return HttpResponse(template.render())


def returns(request):
    template= loader.get_template('staff/returns.html')
    return HttpResponse(template.render())



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff:homepage')  # Redirect to a new URL
    else:
        form = ContactForm()
    return render(request, 'staff/contact.html', {'form': form})




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Redirect users to different dashboards based on their type
            if user.type == 'BUSINESS':
                return redirect('staff:login')  # Redirect to business dashboard
            elif user.type == 'CUSTOMER':
                return redirect('staff:login')  # Redirect to customer dashboard
            messages.success(request, "Registered successfully!")
        else:
            # If form is not valid, display error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            # Optionally, you can log errors for further inspection
            # logger.error(form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'staff/register.html', {'form': form})





def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is authenticated, login the user
            try:
                auth_login(request, user)

                # Redirect users to different dashboards based on their type
                if user.type == 'BUSINESS':
                    return redirect('business:dashboard')  # Redirect to business dashboard
                elif user.type == 'CUSTOMER':
                    return redirect('customer:dashboard')  # Redirect to customer dashboard
            except TypeError as e:
                # Handle the TypeError that might be caused by the missing 'user' argument
                return HttpResponse(f"Error: {str(e)}")
        else:
              # Handle invalid login credentials
            messages.error(request, 'Invalid username or password')
            return render(request, 'staff/login.html')
    else:
        return render(request, 'staff/login.html')
    
@login_required
def update_user(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        
        
        # Get the updated data from the form
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        
        # Update the user information
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        
        # Save the changes
        user.save()

        # Redirect to the user profile page
        return redirect('staff:profile_redirect')
    
    # If the request method is GET, render the user information update form
    else:
        return render(request, 'staff/update_user.html')
    
@login_required   
def profile_redirect(request):
    if request.user.type == 'BUSINESS':
        return redirect('business:profile')
    elif request.user.type == 'CUSTOMER':
        return redirect('customer:profile')
    

@login_required
def account(request):
    # Get the currently logged-in user
    current_user = request.user

    # Access user information directly from the user object
    user_context = {
        'username': current_user.username,
        'email': current_user.email,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
    }

    # Fetch profile data if exists
    try:
        profile = Profile.objects.get(user=current_user)
        profile_context = {'profile': profile}
    except Profile.DoesNotExist:
        profile_context = {}

    # Combine user and profile context
    context = {**user_context, **profile_context}

    if request.user.type == 'BUSINESS':
        return render(request, 'business/account.html', context)
    elif request.user.type == 'CUSTOMER':
        return render(request, 'customer/account.html', context)
    
    
def index(request):
    template = loader.get_template('staff/index.html')
    return HttpResponse(template.render())

def about(request):
    template = loader.get_template('staff/about.html')
    return HttpResponse(template.render())

def FAQS(request):
    template = loader.get_template('staff/FAQS.html')
    return HttpResponse(template.render())

def homepage(request):
    template=loader.get_template('staff/homepage.html')
    return HttpResponse(template.render())

def services(request):
    template=loader.get_template('staff/services.html')
    return HttpResponse(template.render())

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        print('logged out from websites..')
        return redirect('staff:login')  
    else:
        return render(request, 'staff/logout.html') 
    
def web_settings(request):
    return render (request, 'staff/settings.html')