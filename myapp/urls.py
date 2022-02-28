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
    path('game/delete/<int:pk>', views.GameDeleteView.as_view(), name='delete_game'),
    path('game/undelete/<int:game_id>', views.game_undelete, name='game_undelete'),
    path('game/add', views.GameCreateView.as_view(), name="game_add"),
    path('game/print', views.print_game, name="print_game"),
    path('category/<int:category_id>', views.category_page),
    path('category/add', views.CategoryCreateView.as_view(), name="category_add"),
    path('category/edit/<int:pk>', views.CategoryUpdateView.as_view(), name="update_category"),
    path('category/delete/<int:pk>', views.CategoryDeleteView.as_view(), name="delete_category"),
    path('category/deleted', views.category_deleted),
    path('export', views.export_csv, name='export_csv'),
    path('import', views.import_csv, name='import_csv'),
    path('login', views.login_page, name='login_page'),
    path('register', views.register_page, name='register_page'),
    path('logout', views.logout_user, name='logout'),
    path('api-call', views.api_call, name='api_call'),
]
