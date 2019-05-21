from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RecipeCreateForm, StepModelFormset
from users.models import User
from recipe.models import Recipe
from steps.models import Step
# Create your views here.

def new_recipe_view(request,*args,**kwargs):
    form = RecipeCreateForm(request.POST or None)
    formset = StepModelFormset(request.POST or None,request.FILES or None)
    if form.is_valid() and formset.is_valid():
        recipe = form.save(commit=False)
        mainImage = request.FILES['mainImage']
        recipe.fk_user = User.objects.get(id=36) #TODO: take the user from session
        recipe.mainImage = mainImage
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
                print("INVALID FORM IN FORMSET")
        #FORMSET TESTING END
        form = RecipeCreateForm()
        return HttpResponseRedirect('/success/url/')
    context = {
        'form':form,
        'formset':formset
    }
    return render(request,'recipe/new_recipe.html',context)