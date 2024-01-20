from django.shortcuts import redirect, render
from django.http import HttpResponse

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
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
    if request.method == 'POST': 
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