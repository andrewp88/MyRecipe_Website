from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RecipeCreateForm, StepModelFormset, SearchForm
from users.models import User
from recipe.models import Recipe
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render , get_object_or_404 , redirect
from steps.models import Step
# Create your views here.

def new_recipe_view(request,*args,**kwargs):
    if (request.user.is_authenticated):
        userId = request.user.id
        if request.method == 'POST':
            form = RecipeCreateForm(request.POST or None,request.FILES or None)
            formset = StepModelFormset(request.POST or None,request.FILES or None)
            if form.is_valid() and formset.is_valid():
                recipe = form.save(commit=False)
                recipe.fk_user = User.objects.get(id=userId)
                recipe.save()
                rec = Recipe.objects.filter(fk_user_id=recipe.fk_user.id).filter(title=recipe.title).last()
                #FORMSET TESTING BEGIN
                stepNumber = 0
                for f in formset:
                    if f.is_valid():
                        stepNumber +=1
                        print("FORMSET IS VALID Description:")
                        step = f.save(commit=False)
                        step.recipe = rec
                        step.order = stepNumber
                        step.save()
                        formset = StepModelFormset()
                    else:
                        print (f.non_field_errors())
                        messages.error(request,"error")
                        print("INVALID FORM IN FORMSET")
                #FORMSET TESTING END
                return HttpResponseRedirect('../myrecipe/')
            else:
                print("INVALID FORM OR TOTAL FORMSET")
        else:
            form = RecipeCreateForm()
            formset = StepModelFormset()
        context = {'form':form,
                    'formset': formset}
        return render(request,'recipe/new_recipe.html',context)
    else:
        raise PermissionDenied




def my_recipe_view(request):
    if request.user.is_authenticated:
        userId = request.user.id
        queryset = Recipe.objects.filter(fk_user_id=userId)
        paginator = Paginator(queryset, 9)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        context = {
            "recipe_list":recipes
        }
        return render(request,'recipe/myRecipe.html',context)
    else:
        raise PermissionDenied


def saved_recipe_view(request):
    form = SearchForm(request.GET)
    recipes=[]

    if(request.GET.get("searchInput")):
        if form.is_valid():
            searchInput=request.GET["searchInput"]
            recipes = Recipe.objects.filter(title=searchInput)

    context = {"form":form,"recipes":recipes}
    return render(request,'recipe/savedRecipe.html',context)


def detail_recipe_view(request,my_id):
    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe,id=my_id)
        if (recipe.shared or (recipe.fk_user.id == request.user.id)): #check the rights of the user to see this recipe, or it is shared or it is your property
            context = {
                "recipe":recipe
            }
            return render(request,"recipe/recipeDetail.html",context)
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied


def delete_recipe_view(request,my_id):
    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe,id=my_id)
        if (recipe.fk_user.id == request.user.id): #checks if the user have the authorization to delete or view that recipe.
            context ={
                "recipe":recipe
            }
            if request.method == "POST":  #check the user to confirm the deletion of the recipe
                recipe.delete()
                return redirect("../../../myrecipe")
            return render(request,"recipe/recipeDelete.html",context)
    else:
        raise PermissionError