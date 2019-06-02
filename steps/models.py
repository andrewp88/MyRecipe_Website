from django.db import models

# Create your models here.

class Step(models.Model):
    description = models.CharField(max_length=350)
    img1 = models.ImageField(upload_to='recipes/steps/')
    img2 = models.ImageField(upload_to='recipes/steps/')
    order = (models.DecimalField(max_digits=2,decimal_places=0,default=0))
    recipe = models.ForeignKey(
        'recipe.Recipe',
        related_name='recipe_set',
        on_delete=models.CASCADE,
    )