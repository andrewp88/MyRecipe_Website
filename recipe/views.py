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
    if request.user.is_authenticated:
        form = SearchForm(request.GET)
        recipes=[]

        if(request.GET.get("searchInput")):
            if form.is_valid():
                searchInput=request.GET["searchInput"]
                recipes = Recipe.objects.filter(title__icontains=searchInput)

        context = {"form":form,"recipes":recipes}
        return render(request,'recipe/savedRecipe.html',context)
    else:
        raise PermissionDenied

def homepage(request):
    form = SearchForm(request.GET)
    querySet=[]

    if(request.GET.get("searchInput")):
        if form.is_valid():
            searchInput=request.GET["searchInput"]
            querySet=splitSearchInput(searchInput)

    else: querySet=Recipe.objects.filter(shared=True)

    paginator = Paginator(querySet, 12)
    page = request.GET.get('page')
    recipe_list = paginator.get_page(page)

    context = {"form":form,"recipe_list":recipe_list}
    return render(request,'recipe/homepage.html',context)

def splitSearchInput(searchInput):
    searchInp=searchInput.replace(" ", "")
    print(searchInp)
    result= searchInp.split(",")
    return querySetCreation(result)

def querySetCreation(searchInput):
    counter=0;
    print("searchInput: ",searchInput)
    querySetU=Recipe.objects.none() #querySetUnion che mi servirà per mettere insieme i risultati di tutti gli input
    querySetInt=Recipe.objects.none() #querySetIntersection per gestire le intersection

    if(len(searchInput)==1): #caso in cui c'è solo un elemento nella barra di ricerca
        print("input: ",searchInput[0])
        querySetT = Recipe.objects.filter(title__icontains=searchInput[0])
        querySetC = Recipe.objects.filter(fk_category__title__icontains=searchInput[0])
        querySetI = Recipe.objects.filter(ingredients__icontains=searchInput[0])
        querySetIU =querySetT.union(querySetC).union(querySetI)
        querySetU= querySetU.union(querySetIU)


    else:
        for input in searchInput: #per ogni elemento nella barra di ricerca
                print("INPUT: ",input)
                querySetT = Recipe.objects.filter(title__icontains=input) #querySet confrontato con tutti i titoli
                querySetI = Recipe.objects.filter(ingredients__icontains=input)#querySet confrontato con tutti gli ingredienti

                if(not querySetInt.count()): #se il set di intersection è vuoto, quindi all'inizio
                    print("querySetNone")
                    if(querySetT.count() and querySetI.count()): #se entrambi sono pieni
                        querySetInt=querySetT.union(querySetI) #faccio un intersection
                        print("querySetInt both T and I full:", querySetInt)
                    elif(querySetI.count()): #se solo uno dei due è pieno setto il querySetIntersection a quello
                        querySetInt=querySetI
                        print("querySetInt solo I è full:", querySetI)

                    elif(querySetT.count()):
                        querySetInt=querySetT
                        print("querySetInt solo T è full:", querySetT)
                else: #caso in cui il quesrySetInt non sia vuoto
                    print("querySetInt è stato settato")

                    if(querySetT.count() or querySetI.count()):
                        print("querySetInt è stato settato T o I sono pieni")

                        querySetCheckT=querySetInt.intersection(querySetT)
                        print("intersezione con I:",querySetCheckT)


                        querySetCheckI=querySetInt.intersection(querySetI)
                        print("intersezione con T: ",querySetCheckI)

                        if(querySetCheckT.count() and querySetCheckI.count()):
                            querySetCheckFinal=querySetInt.intersection(querySetCheckT).intersection(querySetCheckI)
                            if(querySetCheckFinal.count()):
                                querySetInt=querySetCheckFinal
                            else:
                                counter=0
                                querySetInt=Recipe.objects.none()
                                return querySetInt
                        elif(querySetCheckT.count()):
                            counter+=1
                            querySetInt=querySetCheckT
                        elif(querySetCheckI.count()):
                            counter+=1
                            querySetInt=querySetCheckI
                        else:
                            counter=0
                            querySetInt=Recipe.objects.none()
                            return querySetInt
                    else:
                        counter=0
                        querySetInt=Recipe.objects.none()
                        return querySetInt




        if(counter>0):
            querySetU=querySetInt


    querySet=querySetU.filter(shared=True)
    print("querySet:",querySet)
    counter=0
    return querySet

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
