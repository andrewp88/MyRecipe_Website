from django import forms
from .models import Recipe
from categories.models import Category
from steps.models import Step
from django.forms import modelformset_factory
from django.forms import inlineformset_factory


class SearchForm(forms.Form):
    searchInput=forms.CharField(
        max_length="50",
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Title, category, ingredients..", "class":"form-control form-control mr-3"}))
    class Meta:
        fields=[
            'searchInput'
        ]

class RecipeCreateForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={"placeholder": "Your recipe title"}),
        required=True
    )
    mainImage=forms.ImageField(
        label="Recipe Presentation Image:",
        widget=forms.FileInput(),
        required=False,
    )
    portions = forms.CharField(
        label='Portions',
        widget=forms.TextInput(attrs={"placeholder": "for 3 person / 12 biscuits"}),
        required=True
    )
    ingredients = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "2 eggs,30g of sugar,300ml of skimmed milk",
                "class": "new-class-name two",
                "id": "my-id-for-textarea",
                "rows": 5,
                'cols': 6
            }
        )
    )
    prepTime = forms.DecimalField(
        label='Preparation time',
        initial=0,
        widget=forms.NumberInput(attrs={'step':'1','min':'0','max':'300'})
    )
    cookTime = forms.DecimalField(
        label='Cooking time',
        initial=0,
        widget=forms.NumberInput(attrs={'step':'1','min':'0','max':'300'})
    )
    difficulties = (('1','Very Easy'),('2','Easy'),('3','Medium'),('4','Hard'),('5','Very Hard'))
    difficulty = forms.ChoiceField(initial=0,
        widget=forms.Select,
        choices=difficulties
    )
    shared = forms.BooleanField(initial=False,
        label="Public recipe",
        required=False,
        widget = forms.CheckboxInput(),
    )
    fk_category = forms.ModelChoiceField(
        label='Recipe Category',
        queryset=Category.objects.all(),
        initial=0,
    )

    def __init__(self, *args, **kwargs):
        super(RecipeCreateForm, self).__init__(*args, **kwargs)
        self.initial['fk_user'] = 0

    class Meta:
        model = Recipe
        fields = [
            'title',
            'mainImage',
            'ingredients',
            'prepTime',
            'cookTime',
            'difficulty',
            'portions',
            'fk_category',
            'shared',
        ]

class StepCreateForm(forms.ModelForm):
    class Meta:
        model = Step
        exclude = ('order',)

    description = forms.CharField(
        label="Step Procedure",
        required=True,
        widget=forms.TextInput(attrs={
            "rows": 5,
            'cols': 6,
            'placeholder': 'Write the preparation step of the recipe here'
        })
    )

    img1 = forms.ImageField(
        label="Image 1",
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput(),
        required=False)

    img2 = forms.ImageField(
        label="Image 2",
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput(),
        required=False)


StepCreateFormSet = inlineformset_factory(Recipe,Step,form=StepCreateForm,extra=1)



