from django.db import models

# Create your models here.

class Step(models.Model):
    description = models.CharField(max_length=250)
    img1 = models.ImageField(upload_to='recipes/steps/')
    img2 = models.ImageField(upload_to='recipes/steps/')
    order = (models.DecimalField(max_digits=2,decimal_places=0))
    recipe = models.ForeignKey(
        'recipe.Recipe',
        on_delete=models.CASCADE,
    )