from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,name,surname,dateofbirth,username,country,email,profileImg = None ,is_admin=False,is_active=True,password=None,):
        if not username:
            raise ValueError("user must have a username")
        if not email:
            raise ValueError("user must have an email")
        if not password:
            raise ValueError("user must have a password")
        user_obj=self.model(
            email=self.normalize_email(email)
        )
        user_obj.name=name
        user_obj.surname=surname
        user_obj.username=username
        user_obj.dateofbirth=dateofbirth
        user_obj.profileImg=profileImg
        user_obj.country=country
        user_obj.set_password(password)
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save()

        return user_obj





class User(AbstractBaseUser):

    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    dateofbirth = models.DateField()
    registrationDate = models.DateField().auto_now_add
    username=models.CharField(max_length=70)
    profileImg = models.ImageField(upload_to='users/',default='users/not-user.png')
    country = models.CharField(max_length=35 , default="Europe")
    email = models.EmailField(unique=True)
    admin=models.BooleanField(default=False)
    active=models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','surname','dateofbirth','username','profileImg','country']


    def __str__(self):
        return self.email

    def get_name(self):
        return self.name

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    #def save(self, *args, **kwargs):
     #   self.password = make_password(self.password)
      #  super(User, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return f"/user/{self.id}"

