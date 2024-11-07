from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, 'You have successfully logged in to your account')
            return redirect('event-home-page')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')

    else:
        return render(request, 'authenticate/login.html')
    
def logout_user(request):
    logout(request)
    messages.info(request, 'You have successfully logged out of your account')
    return redirect('event-home-page')

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration Successful!')
            return redirect('login')  # Redirect to your desired page
        else:
            messages.error(request, 'Registration not successful. Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'authenticate/sign_up.html', {'form': form})



