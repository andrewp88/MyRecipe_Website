from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RecipeCreateForm, StepModelFormset
from users.models import User
from recipe.models import Recipe
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
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
        paginator = Paginator(queryset, 3)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        context = {
            "recipe_list":recipes
        }
        return render(request,'recipe/myRecipe.html',context)
    else:
        raise PermissionDenied


def saved_recipe_view(request):
    context = {}
    return render(request,'recipe/savedRecipe.html',context)