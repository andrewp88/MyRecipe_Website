from django.urls import path
from . import views

urlpatterns = [
    path('newrecipe/',views.new_recipe_view,name='newrecipe'),
    path('myrecipe/',views.my_recipe_view,name='myrecipe'),
    path('savedrecipe/',views.saved_recipe_view,name='savedrecipe'),

]