from django.db import models

# Create your models here.

class Step(models.Model):
    description = models.CharField(max_length=250)
    img1 = models.ImageField()
    img2 = models.ImageField()
    recipe = models.ForeignKey(
        'recipe.Recipe',
        on_delete=models.CASCADE,
    )