from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=35)

    def __str__(self):
        return u'{0}'.format(self.title)