from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
# Create your views here.
def index(request):
    con=Product.objects.all()
    return render(request,"newapp/index.html",{"con":con})
def singlecourse_detail(request, pk):
    singlecourse = get_object_or_404(Product, pk=pk)

    
    return render(request, "newapp/course-single.html", {"sin": singlecourse})






def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
          
            return redirect('login')
        else:
          
            return render(request, 'newapp/register.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'newapp/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Replace 'home' with the appropriate URL name for your homepage
    return render(request, 'newapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')