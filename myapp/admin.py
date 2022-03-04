from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CreateUserForm, ChangeUserForm, User

# Register your models here.
from .models import Game, Category, Favorite, SavedGame

CUser = get_user_model()

admin.site.register(Category)
admin.site.register(Game)
admin.site.register(Favorite)
admin.site.register(SavedGame)

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CreateUserForm
    form = ChangeUserForm
    model = User
    list_display = ['username', 'email', 'developer']


admin.site.register(User, CustomUserAdmin)
