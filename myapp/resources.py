from import_export import resources
from .models import Game

class GameResource(resources.ModelResource):
    class Meta:
        model = Game
