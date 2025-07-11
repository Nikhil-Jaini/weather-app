from django.db import models

class SearchHistory(models.Model):
    city = models.CharField(max_length=100)
    date_searched = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city
# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name
