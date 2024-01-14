from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import UserForm
from .models import User
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