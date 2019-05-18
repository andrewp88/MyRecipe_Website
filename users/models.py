from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,name,surname,dateofbirth,username,profileImg,country,email,is_admin=False,is_active=True,password=None,):
        if not username:
            raise ValueError("user must have a username")
        user_obj=self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.admin=is_admin
        user_obj.active=is_active
        user_obj.name=name
        user_obj.surname=surname
        user_obj.dateofbirth=dateofbirth
        user_obj.profileImg=profileImg
        user_obj.country=country
        user_obj.save(using=self._db)

        return user_obj





class User(AbstractBaseUser):
    USERNAME_FIELD='email'

    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    dateofbirth = models.DateField()
    registrationDate = models.DateField().auto_now_add
    username=models.CharField(max_length=70)
    profileImg = models.ImageField(default='/static/imgs/not-user.jpg')
    country = models.CharField(max_length=35 , default="Europe")
    email = models.EmailField(unique=True)
    admin=models.BooleanField(default=False)
    active=models.BooleanField(default=True)

    REQUIRED_FIELDS = ['name','surname','dateofbirth','username','profileImg','country']


    def __str__(self):
        return self.email


    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    #def save(self, *args, **kwargs):
     #   self.password = make_password(self.password)
      #  super(User, self).save(*args, **kwargs)




