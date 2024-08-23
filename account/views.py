from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect

def logout_view(request) :
    logout(request)
    messages.success(request, 'Logged out successful')
    return HttpResponseRedirect(reverse('home'))

def login_view(request) :
    if request.method == 'POST' :
        email = request.POST.get('email')
        username = email.split('@')[0]
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user != None :
            if user.is_active :
                login(request, user)
                messages.success(request, f'Logged in as {username}')
                return HttpResponseRedirect(reverse('home'))
            else :
                messages.error(request, 'This account is disabled')
                return render(request, 'login.html')
        else :
            messages.error(request, 'This account does not Exist')
            return render(request, 'login.html')

    else :
        return render(request, 'login.html')

def register(request) :
    if request.method == 'POST' :
        try:
            email = request.POST.get('email')
            username = email.split('@')[0]
            password = request.POST.get('password')

            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

            messages.success(request, f'Account for {username} created successfully')
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        except :
            messages.error(request, 'An error occured')
            return HttpResponseRedirect(reverse('register'))
    else :
        return render(request,'register.html')