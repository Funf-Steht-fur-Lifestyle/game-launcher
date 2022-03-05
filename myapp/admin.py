from django.contrib import admin

# Register your models here.
from .models import Game, Category, Favorite, SavedGame
# admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Game)
admin.site.register(Favorite)
admin.site.register(SavedGame)
