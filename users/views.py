from django.shortcuts import render
from .models import User
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages






def user_registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            #form.save()
            username = form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            messages.success(request,f'account created for {username}!')
            raw_password = form.cleaned_data.get('password')
            encrPass=make_password(raw_password)
            print("usernam: ",username,"  passw: ",raw_password)


            user = form.save(commit=False)
            print("UUUser",user)


            #user.password = encrPass
            user.active=True
            user.admin=False
            user.save()

            #user = User.objects.create_user(username=username, password=encrPass)
            u = authenticate(username=email, password=raw_password)
            print("user: ",u)
            if(u !=None):
                login(request, u)
                return redirect('/home')
            else:
                return render(request, 'users/user_registration.html', {'form': form})



    form = UserRegistrationForm()
    return render(request, 'users/user_registration.html', {'form': form})



def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            encrPass=make_password(raw_password)
            #user = User.objects.create_user(username=username, password=encrPass)
            u = authenticate(username=username, password=encrPass)
            print("user: ",u)
            if(u !=None):
                login(request, u)

                print("user:",u)
                return redirect('/home')
           # else:
            #s    return render(request, 'users/user_registration.html', {'form': form})

    form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})



