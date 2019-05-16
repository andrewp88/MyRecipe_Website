from django.urls import path
from . import views

urlpatterns = [
    path('',views.new_recipe_view,name='new_recipe_view')
]