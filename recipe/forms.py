from django import forms
from .models import Recipe
from categories.models import Category
from steps.models import Step
from django.forms import modelformset_factory

class RecipeCreateForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={"placeholder": "Your recipe title"}),
        required=True
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
                "placeholder": "Your description",
                "class": "new-class-name two",
                "id": "my-id-for-textarea",
                "rows": 2,
                'cols': 10
            }
        )
    )
    prepTime = forms.DecimalField(
        initial=0,
        widget=forms.NumberInput(attrs={'step':'1','min':'0','max':'300'})
    )
    cookTime = forms.DecimalField(
        initial=0,
        widget=forms.NumberInput(attrs={'step':'1','min':'0','max':'300'})
    )
    difficulties = (('1','Very Easy'),('2','Easy'),('3','Medium'),('4','Hard'),('5','Very Hard'))
    difficulty = forms.ChoiceField(initial=0,
        widget=forms.Select,
        choices=difficulties
    )
    shared = forms.BooleanField(initial=False,
        required=False,
        widget = forms.CheckboxInput()
    )
    fk_category = forms.ModelChoiceField(queryset=Category.objects.all(),
        initial=0
    )

    def __init__(self, *args, **kwargs):
        super(RecipeCreateForm, self).__init__(*args, **kwargs)
        self.initial['fk_user'] = 0

    class Meta:
        model = Recipe
        fields = [
            'title',
            'ingredients',
            'prepTime',
            'cookTime',
            'difficulty',
            'portions',
            'shared',
            'fk_category',
        ]

StepModelFormset = modelformset_factory(
    Step,
    fields=('description','img1','img2',),
    extra=1,
    widgets={
        'description': forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Enter the step description here'
        })
    }
)