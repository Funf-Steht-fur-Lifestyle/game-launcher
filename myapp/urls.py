from django.urls import path

from . import views

# Define URLs for your application.
# 
# Every URL path is based on the URL location, method in a
# views file, and optionally a name, that will refer to the
# URL location, for example:
# 
# path('', views.index, name='index')
# the index will point to http://localhost/

urlpatterns = [
    path('', views.index, name='index'),
    path('game/<int:game_id>', views.game_by_id, name='game_by_id'),
    path('game/edit/<int:pk>', views.GameUpdateView.as_view(), name='update_game'),
    path('game/delete/<int:game_id>', views.game_delete, name='delete_game'),
    path('game/undelete/<int:game_id>', views.game_undelete, name='game_undelete'),
    path('game/mark_favorite/<int:game_id>/<int:user_id>', views.mark_game_as_favorite, name='mark_game_as_favorite'),
    path('game/save/<int:game_id>/<int:user_id>', views.save_game_to_library, name='save_game_to_library'),
    path('category/saved', views.saved_games_page, name='saved_games_page'),
    path('category/saved/<int:saved_game_id>', views.saved_game_details_page, name='saved_game_details_page'),
    path('game/saved/delete/<int:saved_game_id>', views.delete_game_from_library, name='delete_game_from_library'),
    path('game/unmark_favorite/<int:game_id>/<int:user_id>', views.unmark_game_as_favorite, name='unmark_game_as_favorite'),
    path('game/add', views.GameCreateView.as_view(), name="game_add"),
    path('game/print/<int:game_id>', views.print_game, name="print_game"),
    path('sortBy=<str:value>&sortId=<int:sort_id>', views.sort_games_by, name="sort_games_by"),
    path('category/<int:category_id>', views.category_page, name="category_page"),
    path('category/add', views.CategoryCreateView.as_view(), name="category_add"),
    path('category/edit/<int:pk>', views.CategoryUpdateView.as_view(), name="update_category"),
    path('category/delete/<int:category_id>', views.category_delete, name="delete_category"),
    path('category/deleted', views.category_deleted, name="category_deleted"),
    path('category/favorites', views.category_favorites_page, name="category_favorites_page"),
    path('export', views.export_csv, name='export_csv'),
    path('import', views.import_csv, name='import_csv'),
    path('login', views.login_page, name='login_page'),
    path('register', views.register_page, name='register_page'),
    path('logout', views.logout_user, name='logout'),
    path('api-call', views.api_call, name='api_call'),
    path('api-call-search-game', views.igdb_api_search_game, name='igdb_api_search_game')
]
