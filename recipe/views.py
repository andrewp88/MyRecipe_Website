from django.shortcuts import render
from .forms import RecipeCreateForm, StepModelFormset
from users.models import User
from steps.models import Step
# Create your views here.

def new_recipe_view(request,*args,**kwargs):
    form = RecipeCreateForm(request.POST or None)
    formset = StepModelFormset(request.POST)
    if form.is_valid():
        recipe = form.save(commit=False)
        print(type(recipe))
        recipe.fk_user = User.objects.get(id=1) #TODO: take the user from session
        recipe.save()
        form = RecipeCreateForm()
    context = {
        'form':form,
        'formset':formset
    }
    return render(request,'recipe/new_recipe.html',context)