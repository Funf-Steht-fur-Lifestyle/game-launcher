from django.db import models
from django.contrib.auth.models import User

from mysite import settings

from datetime import datetime

# A class represents table in the database.
# It is currently work in progress (WIP).

class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % (self.title)

class Developer(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % (self.name)


class Publisher(models.Model):
    publisher = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % (self.name)


# class User(models.Model):
#     name = models.CharField(max_length=200)
#     password = models.CharField(max_length=200)
# 
#     def __str__(self):
#         return '%s' % (self.name)


class Game(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='img/', blank=True)
    desc = models.TextField("Description")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, default=0)
    # developer = models.ForeignKey(Developer, on_delete=models.CASCADE, default=0)
    # publication_date = models.DateTimeField(default=datetime.now, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.name)


# class Favorite(models.Model):
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.game)
