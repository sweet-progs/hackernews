from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    created = models.CharField(max_length=200)

    # def __str__(self):
    #     return str({self.id, self.title, self.url, self.created})