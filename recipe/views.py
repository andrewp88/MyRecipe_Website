from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RecipeCreateForm, StepCreateFormSet , SearchForm
from users.models import User
from recipe.models import Recipe
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render , get_object_or_404 , redirect
from steps.models import Step
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
# Create your views here.




def my_recipe_view(request):
    if request.user.is_authenticated:
        userId = request.user.id
        queryset=Recipe.objects.filter(fk_user_id=userId)
        if(not queryset.count()):
            messages.add_message(request, messages.INFO, 'You have not created any recipe yet.')


        form = SearchForm(request.GET)
        if(request.GET.get("searchInput")):
            if form.is_valid():
                searchInput=request.GET["searchInput"]
                arraySearch=splitSearchInput(searchInput)
                if(len(arraySearch)>5):
                    messages.add_message(request, messages.INFO, 'You can search up to 5 words.')
                    return redirect('/home')
                else:
                    querySetS=Recipe.objects.filter(fk_user_id=userId)
                    querySetTem=querySetCreation(arraySearch).order_by('-id')
                    queryset=querySetS.intersection(querySetTem)
                    if(not queryset.count()):
                        messages.add_message(request, messages.INFO, 'There are no recipes matching your search.')


        paginator = Paginator(queryset, 9)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        context = {
            "form":form,
            "recipe_list":recipes
        }
        return render(request,'recipe/myRecipe.html',context)
    else:
        messages.add_message(request, messages.INFO, 'You have to login in order to access the page')
        return redirect('/login')


def saved_recipe_view(request):
    if request.user.is_authenticated:
        user=request.user
        recipes=user.savedRecipes.all()
        if(not recipes.count()):
            messages.add_message(request, messages.INFO, 'There are no saved recipes at the moment.')

        context = {"recipe_list":recipes}
        return render(request,'recipe/savedRecipe.html',context)
    else:
        messages.add_message(request, messages.INFO, 'You have to login in order to access the page')
        return redirect('/login')

def userRecipe(request,my_id):
    user = get_object_or_404(User,id=my_id)
    queryset = Recipe.objects.filter(fk_user_id=my_id).order_by('-id')
    paginator = Paginator(queryset, 9)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    context = {
        "recipeUser":user,
        "recipe_list":recipes
    }
    return render(request,"recipe/userRecipe.html",context)

def homepage(request):
    form = SearchForm(request.GET)
    querySet=[]
    arraySearch=[]

    if(request.GET.get("searchInput")):
        if form.is_valid():
            searchInput=request.GET["searchInput"]
            arraySearch=splitSearchInput(searchInput)
            if(len(arraySearch)>5):
                messages.add_message(request, messages.INFO, 'You can search up to 5 words.')
                return redirect('/home')
            else:
                querySetS=Recipe.objects.filter(shared=True)
                querySetTem=querySetCreation(arraySearch).order_by('-id')
                querySet=querySetS.intersection(querySetTem)
                if(not querySet.count()):
                    messages.add_message(request, messages.INFO, 'There are no recipes matching your search.')


    else: querySet=Recipe.objects.filter(shared=True).order_by('-id')
    if(not querySet.count()):
        messages.add_message(request, messages.INFO, 'There are no shared recipes at the moment.')


    paginator = Paginator(querySet, 12)
    page = request.GET.get('page')
    recipe_list = paginator.get_page(page)

    context = {"form":form,"recipe_list":recipe_list}
    return render(request,'recipe/homepage.html',context)

def splitSearchInput(searchInput):
    searchInp=searchInput.replace(" ", "")
    result= searchInp.split(",")
    return result

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


    counter=0
    return querySetU

def detail_recipe_view(request,my_id):
    recipe = get_object_or_404(Recipe,id=my_id)
    steps = Step.objects.filter(recipe__id=my_id).order_by('id')
    if (recipe.shared or ( request.user.is_authenticated and recipe.fk_user.id == request.user.id)): #check the rights of the user to see this recipe, or it is shared or it is your property
        context = {
            "recipe":recipe,
            "steps":steps
        }
        return render(request,"recipe/recipeDetail.html",context)
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


def saveRecipe(request,my_id): #ADD A RECIPE TO SAVED OR REMOVES IT FROM SAVED
    if request.user.is_authenticated:
        recipe = get_object_or_404(Recipe,id=my_id)
        user=request.user
        html = "empty"
        if( user.savedRecipes.filter(id=recipe.id).exists()):
            user.savedRecipes.remove(recipe)
            html = "<h1>removed</h1>"
        else:
            user.savedRecipes.add(recipe)
            html = "<h1>saved</h1>"
    return HttpResponse(html)


class RecipeCreateView(LoginRequiredMixin,CreateView):
    template_name = "recipe/new_recipe.html"
    model = Recipe
    form_class = RecipeCreateForm
    #fields = ['mainImage','title','ingredients','portions','fk_category','difficulty','prepTime','cookTime','shared']
    success_url = reverse_lazy('myrecipe')

    def get_context_data(self, **kwargs): #gets the data from the formset
        data = super(RecipeCreateView,self).get_context_data(**kwargs)
        if self.request.POST:
            data['steps'] = StepCreateFormSet(self.request.POST,self.request.FILES or None)
        else:
            data['steps']= StepCreateFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        steps = context['steps']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.fk_user = self.request.user
            self.object.save()

            if steps.is_valid():
                steps.instance = self.object
                steps.save()
            else:
                print("INVALID STEPS FORM")
        return super(RecipeCreateView,self).form_valid(form)



