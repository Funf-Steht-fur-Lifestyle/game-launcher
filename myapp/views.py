from django.shortcuts import render

import requests
import csv

from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView

from tablib import Dataset

from .models import Game, Category
from .resources import GameResource
from .forms import GameForm, CategoryForm, CreateUserForm

# This fiels contains the logic for the URLs i. e. it tells what
# should be represented by the browser. For example loading an
# index.html file or making the HTTP GET/POST request to the API.

# Every method in this file, that requires for the user to be logged
# in to access it, must contain the @login_required(login_url='/app/login')
# annotation. Otherwise the user, that is not logged in will be able to
# access it.
#
# This approach is quite messy and it should be replaced by the MIDDLEWARE
# approach. This will be done, when I figure out how it works.

@login_required(login_url='/app/login')
def index(request):
    categories = Category.objects.all()
    games = Game.objects.filter(deleted=False)

    args = {}
    args['categories'] = categories
    args['games'] = games

    return render(request, 'index.html', args)


@login_required(login_url='/app/login')
def game_by_id(request, game_id):
    game = Game.objects.get(pk=game_id)
    categories = Category.objects.all()

    args = {}
    args['game'] = game
    args['categories'] = categories

    return render(request, 'game_details.html', args)


@login_required(login_url='/app/login')
def game_delete(request, game_id):
    game = Game.objects.get(pk=game_id)
    game.deleted = True
    game.save()

    return HttpResponseRedirect('/app/')


@login_required(login_url='/app/login')
def game_undelete(request, game_id):
    game = Game.objects.get(pk=game_id)
    game.deleted = False
    game.save()

    return HttpResponseRedirect('/app/category/deleted')


@login_required(login_url='/app/login')
def category_page(request, category_id):
    categories = Category.objects.all()
    games = Game.objects.filter(category=category_id, deleted=False)

    args = {}
    args['categories'] = categories
    args['games'] = games

    return render(request, 'category_page.html', args)


@login_required(login_url='/app/login')
def category_deleted(request):
    categories = Category.objects.all()
    games = Game.objects.filter(deleted=True)

    args = {}
    args['categories'] = categories
    args['games'] = games

    return render(request, 'category_deleted.html', args)


@login_required(login_url='/app/login')
def category_delete(request, category_id):
    category = Category.objects.get(pk=category_id)
    category.delete()

    categories = Category.objects.all()
    games = Game.objects.all()

    args = {}
    args['categories'] = categories
    args['games'] = games

    return render(request, 'index.html', args)


# Export does work for the user table, but not for the others.
@login_required(login_url='/app/login')
def export_csv(request):
    game_resource = GameResource()
    dataset = game_resource.export()

    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="games.csv"'

    return response


# Import is still work in progress (WIP).
@login_required(login_url='/app/login')
def import_csv(request):
    if request.method == 'POST':
        game_resource = GameResource()
        dataset = Dataset()
        games = request.FILES['file']

        imported_data = dataset.load(games.read(), format='csv', headers=False)
        result = game_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            game_resource.import_data(dataset, dry_run=False)

    return render(request, 'import.html')


def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/app')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/app')
            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'login.html', context)


@login_required(login_url='/app/login')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/app/login')


# @csrf_exempt is needed for the registration form to work
# correctcly. I do not know as to why, because other forms
# do not require it.
@csrf_exempt
def register_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/app/')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'account was created for ' + user)
                return HttpResponseRedirect('/app/login')

        context = {'form':form}
        return render(request, 'register.html', context)


def api_call(request):
    # url = "https://api.igdb.com/v4/games"
    # header = {
    # "Client-Id":"phutxcabah8hduf96zsx7j62s7wkwn",
    # "Authorization":"Bearer o0gcubnb3xik19uysv2jwsgtglrt6r",
    # "fields":"*",
    # }
    r = requests.post('https://id.twitch.tv/oauth2/token?client_id=phutxcabah8hduf96zsx7j62s7wkwn&client_secret=jlth8qse7y6ndfgiwnzkyeuogwsxx7&grant_type=client_credentials')
    # r = requests.post(url, headers=header)

    print(r)
    print("HTTP Status Code: ", r.status_code)
    print(r.json())

    if r.status_code == 200:
        return HttpResponse('Yay, it worked')
    return HttpResponse('Error')


# For the popups to work, we need to create classes that extend
# the original view (BSModelCreate|Update|DeleteView).
#
# The GameCreateView and CategoryCreateView do work, but the
# update forms do not.
class GameCreateView(BSModalCreateView):
    form_class = GameForm
    template_name = 'game_add.html'
    success_message = 'Success: Game was created.'
    success_url = reverse_lazy('index')


class GameUpdateView(BSModalUpdateView):
    model = Game
    form_class = GameForm
    template_name = 'game_edit.html'
    success_message = 'Success: Game was updated.'
    success_url = reverse_lazy('index')


class CategoryCreateView(BSModalCreateView):
    form_class = CategoryForm
    template_name = 'category_add.html'
    success_message = 'Success: Category was created.'
    success_url = reverse_lazy('index')


class CategoryUpdateView(BSModalUpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_edit.html'
    success_message = 'Success: Category was updated.'
    success_url = reverse_lazy('index')
