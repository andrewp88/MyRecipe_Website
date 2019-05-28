from django.db import models

# Create your models here.

class Recipe(models.Model):
    mainImage = models.ImageField(upload_to='recipes/titleImgs/')
    title = models.CharField (max_length=50)
    difficulty = models.DecimalField(max_digits=1,decimal_places=0)
    prepTime = models.DecimalField(max_digits=3,decimal_places=0)
    cookTime = models.DecimalField(max_digits=3,decimal_places=0)
    ingredients = models.TextField(max_length=400)
    portions = models.CharField(max_length=40)
    shared = models.BooleanField(default=False)
    fk_user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
    )
    fk_category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE,
    )


    def get_absolute_url(self):
        return f"/recipe/{self.id}"

