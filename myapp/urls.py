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
    path('game/edit/<int:game_id>', views.GameUpdateView.as_view(), name='update_game'),
    path('game/delete/<int:game_id>', views.game_delete, name='game_delete'),
    path('game/undelete/<int:game_id>', views.game_undelete, name='game_undelete'),
    path('game/add', views.GameCreateView.as_view(), name="game_add"),
    path('category/<int:category_id>', views.category_page),
    path('category/add', views.CategoryCreateView.as_view(), name="category_add"),
    path('category/edit/<int:category_id>', views.CategoryUpdateView.as_view(), name="update_category"),
    path('category/delete/<int:category_id>', views.category_delete),
    path('category/deleted', views.category_deleted),
    path('export', views.export_csv, name='export_csv'),
    path('import', views.import_csv, name='import_csv'),
    path('login', views.login_page, name='login_page'),
    path('register', views.register_page, name='register_page'),
    path('logout', views.logout_user, name='logout'),
    path('api-call', views.api_call, name='api_call'),
]
