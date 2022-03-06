from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from game_launcher import settings

from datetime import datetime

# A class represents table in the database.
# It is currently work in progress (WIP).

class Category(models.Model):
    title = models.CharField('Kategorie', max_length=200)

    def __str__(self):
        return '%s' % (self.title)


class User(AbstractUser):
    is_developer = models.BooleanField('Entwickler', default=False)
    is_publisher = models.BooleanField('Herausgeber', default=False)

    def __str__(self):
        return '%s' % (self.username)


class Game(models.Model):
    name = models.CharField('Name', max_length=200)
    thumbnail = models.ImageField('Thumbnail', upload_to='img/', default='default-image.jpg', blank=True)
    desc = models.TextField('Beschreibung')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', verbose_name='Kategorie')
    subcategories = models.ManyToManyField(Category, related_name='subcategories', verbose_name='Sub-Kategorien')
    price = models.FloatField('Preis', blank=True, default=0.0)
    developer = models.ForeignKey(User, limit_choices_to=({'is_developer': True}), on_delete=models.DO_NOTHING, verbose_name='Entwickler')
    publisher = models.ForeignKey(User, related_name='publisher', limit_choices_to=({'is_publisher': True}), on_delete=models.DO_NOTHING, verbose_name="Herausgeber")
    publication_date = models.DateTimeField(default=datetime.now, blank=True)
    deleted = models.BooleanField('Gelöscht', default=False)

    def __str__(self):
        return '%s' % (self.name)


    def is_favorite(self):
        favorites = Favorite.objects.all()
        for favorite in favorites:
            if favorite.game.name == self.name:
                return True

        return False

    
    def get_price(self):
        if self.price == 0.0:
            return "kostenlos"

        return "{} €".format(self.price)


class SavedGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s' % (self.game)


class Favorite(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.game)
