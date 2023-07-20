from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,PurchasedProduct
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
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.urls import reverse

# Create your views here
from.models import UserProfile
def index(request):
    con=Product.objects.all()
    return render(request,"newapp/index.html",{"con":con})

@login_required
def singlecourse_detail(request, pk):
    # Retrieve the product based on the provided pk
    product = get_object_or_404(Product, pk=pk)

    # Retrieve the payment status for the specific course and user combination
    user_profile = request.user.userprofile
    try:
        purchased_product = PurchasedProduct.objects.get(user_profile=user_profile, product=product)
        payment_status = purchased_product.payment_status
    except PurchasedProduct.DoesNotExist:
        payment_status = False

    context = {
        'sin': product,  # Rename 'singlecourse' to 'sin' for consistency with the template
        'payment_status': payment_status,
    }

    return render(request, "newapp/course-single.html", context)


# views.py

from .forms import UserProfileForm

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








def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            return render(request, 'newapp/register.html', {'error': 'Username already exists'})

        if password == confirm_password:
            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            # Create a UserProfile for the user
            UserProfile.objects.create(user=user)
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

from django.core.exceptions import ObjectDoesNotExist

@login_required
def profile(request):
    user_profile = request.user.userprofile

    # Retrieve the courses the user has purchased
    try:
        purchased_products = PurchasedProduct.objects.filter(user_profile=user_profile)
        purchased_courses = [p.product for p in purchased_products]
    except ObjectDoesNotExist:
        purchased_courses = []

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
        'purchased_courses': purchased_courses,
    }

    return render(request, 'newapp/profile.html', context)

@login_required
def profile_edit(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'newapp/edit.html', {'form': form})



@login_required
def payment(request, pk=None):
    if pk is not None:
        # Retrieve the price from the model using the provided pk
        product = get_object_or_404(Product, pk=pk)
        price = product.price

        # Initialize the Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))

        # Generate the order ID and amount
        amount = int(price * 100)  # Convert the price to paise
        order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

        # Associate the purchased product with the user's profile
        user_profile = request.user.userprofile
        product.user_profile = user_profile
        product.save()

        # Create an entry in the PurchasedProduct table for the payment status
        PurchasedProduct.objects.create(user_profile=user_profile, product=product, payment_status=False)

        context = {
            'razorpay_key': settings.RAZORPAY_API_KEY,
            'order': order,
            'user': request.user,
            'amount': amount,
            'product_pk': pk,
        }

        return render(request, 'newapp/payment.html', context)
    else:
        return HttpResponse("Please provide a valid product identifier.")


@require_POST
def payment_success(request, pk):
    # Retrieve the order ID from the POST request
    order_id = request.POST.get('razorpay_order_id')

    # Retrieve the product based on the provided pk
    product = get_object_or_404(Product, pk=pk)

    # Update the payment status of the product
    product.payment_status = True
    product.save()

    # Update the payment status for the specific course and user combination
    user_profile = request.user.userprofile
    purchased_product = get_object_or_404(PurchasedProduct, user_profile=user_profile, product=product)
    purchased_product.payment_status = True
    purchased_product.save()

    try:
        # Redirect to the singlecourse_detail view for the specific product
        return redirect(reverse('newapp:singlecourse_detail', kwargs={'pk': pk}))
    except MultipleObjectsReturned:
        # Handle the case where multiple products have the same order_id
        # Log an error or perform any necessary action
        return redirect('newapp:payment_failure')



from django.core.exceptions import MultipleObjectsReturned





from django.views.decorators.http import require_POST





def show_video(request, pk):
    # Retrieve the product based on the provided ID
    product = get_object_or_404(Product, pk=pk)

    # Pass the product to the template for rendering
    return render(request, 'newapp/video.html', {'product': product})

