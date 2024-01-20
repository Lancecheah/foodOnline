from django.shortcuts import redirect, render
from django.http import HttpResponse
from .utils import detectUser

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied



def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Method 1: Create the user using the form
            # password = form.cleaned_data['password']
            # # Why commit=False? Because we need to add the role Vendor or Customer before save
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # # Save the user's form data to the database.
            # user.save()

            # Method 2: Create the user using create user 
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']  
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            # Using Django's messages framework to display one-time notification messages to the user
            messages.success(request, 'Your account has been registered successfully')
            return redirect('registerUser')
        else:
            print("invalid form")
            print(form.errors)
    else:
        form = UserForm()
    context = {'form': form,}
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    elif request.method == 'POST': 
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']  
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            # Why commit=False? Because in the model the User & UserProfile is already saved
            # So we manually save the vendor data
            vendor = v_form.save(commit=False)
            vendor.user = user
            # Since in the "Signal" we are creating the UserProfile when the User is created
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            # Why we are not doing vendor.vendor_name & vendor.vendor_license? cos 
            # v_form = VendorForm(request.POST, request.FILES) will automatically save the data
            vendor.save()
            # Using Django's messages framework to display one-time notification messages to the user
            messages.success(request, 'Your account has been registered successfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print("invalid form")
            print(form.errors)


    else:        
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form, 
        'v_form': v_form,
        }

    return render(request, 'accounts/registerVendor.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        # 'email must be the same as the name in the form'
        email = request.POST['email']
        password = request.POST['password']
        
        # Django already has a built in authentication system
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user) 
            # If you are messages.success, you need to add {% include 'includes/alerts.html' %}in your html
            messages.success(request, 'You are now logged in')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are now logged out')
    return redirect('login')
    
@login_required(login_url='login')    
def myAccount(request):
    # assuming that the user is logged in
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl )

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')