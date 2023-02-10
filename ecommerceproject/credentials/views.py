import random

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from credentials.models import OTP


# Create your views here.

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            u=User.objects.get(username=username,is_active=False)
            if u:
                print(username+'from if u')
                return redirect('credentials:confirm',username)
        except:
            pass
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('shop:allProdCat')
        else:
            messages.info(request,"Invalid username or password")
            return redirect('credentials:login')
    return render(request,'login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('credentials:login')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpass = request.POST['cpass']
        if password == cpass:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exist")
                return redirect('credentials:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exist")
                return redirect('credentials:register')
            else:
                try:
                    subject='OTP Verification'
                    otp=random.randint(100000,999999)
                    message= 'Your OTP: {0}'.format(otp)
                    email_from=settings.EMAIL_HOST_USER
                    recipient_list=[email,]
                    send_mail(subject,message,email_from,recipient_list)
                    otp_db = OTP.objects.create(otp=otp,email=email)
                    user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
                    user.save()
                except:
                    return {}
                return redirect('credentials:login')
        else:
            messages.info(request, "Passwords not match")
            return redirect('credentials:register')
    return render(request, 'register.html')

@login_required(login_url='credentials:login')
def logout(request):
    auth.logout(request)
    return redirect('shop:allProdCat')


def confirm(request,username):
    if request.user.is_authenticated:
        return redirect('credentials:login')
    username=username
    user = get_object_or_404(User,username=username,is_active=True)
    if user:
        return redirect('credentials:login')
    if request.method=='POST':
        user = User.objects.get(username=username)
        otp_u=request.POST['otp']
        print(username+" from if request")
        print(user.email)
        otp_o=OTP.objects.get(email=user.email)
        if otp_u==str(otp_o.otp):
            print('otp match')
            user.is_active='True'
            user.save()
            return redirect('shop:allProdCat')
        else:
            return redirect('shop:allProdCat')
    return render(request, 'confirm_mail.html',{'username':username})
