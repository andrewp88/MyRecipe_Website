from django.urls import path

from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [


    #path('login/',auth_views.LoginView.as_view(template_name='users\login.html'), name='login'),
    path('registration/', views.user_registration_view, name='registration'),
    path('login/', views.user_login_view, name='login'),
    path('account/', views.user_account_view,name='account'),
    path('logout/',views.user_logout_view,name='logout')

]