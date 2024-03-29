from django import forms
from .models import User
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, get_user_model
from PIL import Image

User = get_user_model()



class UserRegistrationForm(forms.ModelForm):
    name=forms.CharField()
    surname=forms.CharField()
    dateofbirth=forms.DateField(label="Date of birth",widget=forms.TextInput(attrs={"placeholder": "YYYY-MM-DD"}))
    country= forms.CharField(initial="Europe")
    username=forms.CharField()
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput,min_length=5)
    passwordCheck=forms.CharField(label="Confirm password",widget=forms.PasswordInput)
    profileImg = forms.ImageField(label="Profile Image",initial='media/imgs/users/not-user.png')


    class Meta:
            model=User
            fields=[
                'name',
                'surname',
                'dateofbirth',
                'country',
                'username',
                'email',
                'password',
                'passwordCheck',
                'profileImg',
            ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already in use")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("A User with this Username already exists")
        return username

    def clean_password(self, *args, **kwargs):
        passw=self.cleaned_data.get("password")
        passwC=self.data.get("passwordCheck")

        if(passw!=passwC):
            raise forms.ValidationError("The two password must be equal")
        return passw

    def clean_profileImg(self):
        img=self.cleaned_data.get("profileImg")
        im = Image.open(img)
        im.verify()









class UserLoginForm(forms.Form):
    username=forms.CharField(label='Email')
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=[
            'username',
            'password'
        ]
