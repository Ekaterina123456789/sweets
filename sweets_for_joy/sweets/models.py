from django.db import models
from django.contrib.auth.models import User


class Catalog(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='media/images/')
    description = models.TextField()
    price = models.IntegerField(null=False)
    date_completed = models.DateTimeField(null=True, blank=True)
    favourite = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

