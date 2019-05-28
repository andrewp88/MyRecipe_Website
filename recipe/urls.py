from django.urls import path
from . import views

urlpatterns = [
    path('newrecipe/',views.RecipeCreateView.as_view(),name='newrecipe'),
    path('myrecipe/',views.my_recipe_view,name='myrecipe'),
    path('savedrecipe/',views.saved_recipe_view,name='savedrecipe'),
    path('',views.homepage,name='homepage'),
    path('home/',views.homepage,name='homepage'),
    path('recipe/<int:my_id>/',views.detail_recipe_view,name="recipe"),
    path('recipe/<int:my_id>/delete/',views.delete_recipe_view,name="deleterecipe"),
    path('user/<int:my_id>/',views.userRecipe,name="userRecipe")

]