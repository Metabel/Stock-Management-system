import random
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from .forms import CustomSignupForm


login_otps = {}
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomSignupForm()

    return render(request, 'signup.html', {'form': form})

def login_with_otp(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            otp=str(random.randint(100000,999999))
            login_otps[username] = otp

            send_mail(
                'Your login code',
                f'Your otp code is:{otp}',
                settings.DEFAULT_FROM_EMAIL,
                ['user.email'],
            )

            request.session['otp_user'] = username
            return redirect('verify_otp')
        return render(request,'login.html', {'error':'Invalid credentials'})
    return render(request,'login.html')

def verify_otp(request):
    if request.method =='POST':
        entered_otp = request.POST.get('otp')
        username = request.session.get('otp_user')

        if username and login_otps.get(username) == entered_otp:
            user = User.objects.get(username=username)
            login(request,user)

            del login_otps[username]
            del request.session['otp_user']

            return redirect('product_list')
        return render(request,'verify_otp.html', {'error':'Invalid OTP'})
    return render(request,'verify_otp.html')
    

def product_list(request):
    products=Product.objects.all()
    return render(request,'product_list.html',{
        'products':products
    })

def add_product(request):
    if request.method =='POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request,'add_product.html',{'form':form})

def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})

 