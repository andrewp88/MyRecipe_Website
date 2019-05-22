from django.shortcuts import render
from .models import User
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login , get_user_model,logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

User = get_user_model()



def user_registration_view(request):
    form = UserRegistrationForm(request.POST or None, request.FILES or None)
    context = {
        "form": form
    }
    if form.is_valid():
        if (request.FILES):
            myfile = request.FILES['profileImg']
            fs = FileSystemStorage()
            filename = fs.save('users/'+myfile.name, myfile)
        else:
            filename= 'users/not-user.png'

        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        name = form.cleaned_data.get('name')
        surname = form.cleaned_data.get('surname')
        dob = form.cleaned_data.get('dateofbirth')
        country = form.cleaned_data.get('country')
        #user creation
        new_user = User.objects.create_user(name,surname,dob,username,country, email,profileImg=filename, password=password)
        login(request, new_user)

        return render(request, "users/account.html", context)

    return render(request, "users/user_registration.html", context)





def user_login_view(request):
    form = UserLoginForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            #encrPass=make_password(raw_password)
            #user = User.objects.create_user(username=username, password=encrPass)
            user = authenticate(username=username, password=raw_password)
            print("user login attempt: ",user)
            if(user !=None):
                login(request, user)
                print("user autentication succes:",user)
                return redirect('/home')
            else:
               return HttpResponseRedirect('/fail/url/')

    form = UserLoginForm()
    return render(request, 'users/login.html', context)

def user_account_view(request):
    return render(request,"users/account.html")


def user_logout_view(request):
    logout(request)

    return redirect('/home')