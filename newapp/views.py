from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay


# Create your views here
from.models import UserProfile
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

@login_required
def profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'newapp/profile.html', {'form': form})


def payment(request, pk=None):
    if pk is not None:
        # Retrieve the price from the model using the provided pk
        product = get_object_or_404(Product, pk=pk)
        price = product.price  # Assuming 'price' is the field name in your Product model

        # Initialize the Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))

        # Generate the order ID and amount
        amount = int(price * 100)  # Convert the price to paise
        order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

        context = {
            'razorpay_key': settings.RAZORPAY_API_KEY,
            'order': order,
            'user': request.user,
            'amount': amount,  # Pass the amount to the template context
        }

        return render(request, 'newapp/payment.html', context)
    else:
        # Handle the case when 'pk' is not provided
        # Redirect or render an appropriate response
        return HttpResponse("Please provide a valid product identifier.")





def show_video(request, pk):
    # Retrieve the product based on the provided ID
    product = get_object_or_404(Product, pk=pk)

    # Pass the product to the template for rendering
    return render(request, 'newapp/video.html', {'product': product})

