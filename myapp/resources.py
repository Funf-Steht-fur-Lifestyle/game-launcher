from import_export import resources

from .models import User, Game, SavedGame, Category, Favorite

class UserResource(resources.ModelResource):
    class Meta:
        model = User


class GameResource(resources.ModelResource):
    class Meta:
        model = Game


class SavedGameResource(resources.ModelResource):
    class Meta:
        model = SavedGame


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class FavoriteResource(resources.ModelResource):
    class Meta:
        model = Favorite
