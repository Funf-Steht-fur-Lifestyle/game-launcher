from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

# Using modal forms for popups.
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Game, Category

# Forms are the interpretation of a model, which can be found
# in a models.py file.
# Forms enables a user to add, edit, and so on i. e. it gives
# a user UI, from which it can fill the form and add (change)
# the data in the database.

class GameForm(BSModalModelForm):
    class Meta:
        model = Game
        fields = {'name', 'thumbnail', 'desc', 'category', 'publication_date'}

class CategoryForm(BSModalModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
