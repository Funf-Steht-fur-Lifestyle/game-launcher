from import_export import resources

from .models import Game, Category

class GameResource(resources.ModelResource):
    class Meta:
        model = Game


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
