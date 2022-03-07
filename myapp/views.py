from django.shortcuts import render

import os
import requests
import csv
import ctypes
import zipfile
import shutil
import PyPDF2
import pdfkit
import webbrowser

from django.urls import reverse_lazy, resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView

from tablib import Dataset

from .models import AccessToken, User, Game, Category, Favorite, SavedGame
from .resources import UserResource, GameResource, CategoryResource, FavoriteResource, SavedGameResource
from .forms import GameForm, CategoryForm, CreateUserForm
from .exporter import Exporter
from .importer import Importer

# This file contains the logic for the URLs i. e. it tells what
# should be represented by the browser. For example loading an
# index.html file or making the HTTP GET/POST request to the API.

# Every method in this file, that requires for the User to be logged
# in to access it, must be marked with the @login_required(login_url='/app/login')
# annotation. Otherwise the User, that is not logged in will be able to
# access it.
#
# This approach is quite messy and it should be replaced by the MIDDLEWARE
# approach. This will be done, when I figure out how it works.

@login_required(login_url='/app/login')
def index(request):
    categories = Category.objects.all()
    games = Game.objects.filter(deleted=False)
    favorites = Favorite.objects.all()

    args = {}
    args['categories'] = categories
    args['games'] = games
    args['favorites'] = favorites

    return render(request, 'core/index.html', args)


@login_required(login_url='/app/login')
def game_by_id(request, game_id):
    game = Game.objects.get(pk=game_id)
    categories = Category.objects.all()
    favorites = Favorite.objects.all()

    args = {}
    args['game'] = game
    args['categories'] = categories
    args['favorites'] = favorites

    return render(request, 'game/page.html', args)

@login_required(login_url='/app/login')
def game_delete(request, game_id):
    game = Game.objects.get(pk=game_id)
    game.deleted = True
    game.save()

    return HttpResponseRedirect('/app/')

@login_required(login_url='app/login')
def igdb_api_authentication(request):

    r = requests.post('https://id.twitch.tv/oauth2/token?client_id=phutxcabah8hduf96zsx7j62s7wkwn&client_secret=jlth8qse7y6ndfgiwnzkyeuogwsxx7&grant_type=client_credentials')

    print(r)
    print("HTTP Status Code: ", r.status_code)
    print(r.json())

    if r.status_code == 200:
        return r.json()["access_token"]
    
    print("Could not authenticate at twitch.tv")
    return 1

# Für das Suchfeld
@login_required(login_url='app/login')
def igdb_api_search_game(request):
 
    print("search Term: " + request.POST["search_game"])

    url = "https://api.igdb.com/v4/games"

    at = AccessToken.objects.get(pk=1).get_access_token()
    
    payload = "search \""+ request.POST["search_game"] + " \";\r\nfields name;\r\n"
    headers = {
        'Authorization': 'Bearer ' + at,
        'Client-ID': 'phutxcabah8hduf96zsx7j62s7wkwn',
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response)
    print("HTTP Status Code: ", response.status_code)
    print(response.json())

    if response.status_code == 200:
        games = []
        for x in response.json():
            games.append(x["name"])

        args = {}
        args["games"] = games
        return render("game/add.html", args)
    
    #print("API Call >search_game< failed for some reason")
    #return 1

@login_required(login_url='app/login')
def igdb_api_get_game_data(request, gameId):
 
    url = "https://api.igdb.com/v4/games"

    payload = "where id = " + gameId + ";\r\nfields id, name,genres.name, cover.*,rating, slug, summary;"
    
    headers = {
        'Authorization': 'Bearer ' + AccessToken.objects.get(pk=1).get_access_token(),
        'Client-ID': 'phutxcabah8hduf96zsx7j62s7wkwn',
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response)
    print("HTTP Status Code: ", response.status_code)
    print(response.json())

    if response.status_code == 200:
        return response.json()[0] # returns a dict object with a lot of fields
    
    print("API Call >get_game_data< failed for some reason")
    return 1

@login_required(login_url='app/login')

def igdb_api_get_cover_art(request, gameId = "1942", size = "720p"):
    
    # Vorhandene Größen: cover_small 	90 x 128 	Fit
    # screenshot_med 	                569 x 320 	Lfill, Center gravity
    # cover_big 	                    264 x 374 	Fit
    # logo_med 	                        284 x 160 	Fit
    # screenshot_big 	                889 x 500 	Lfill, Center gravity
    # screenshot_huge               	1280 x 720 	Lfill, Center gravity
    # thumb 	                        90 x 90 	Thumb, Center gravity
    # micro 	                        35 x 35 	Thumb, Center gravity
    # 720p                          	1280 x 720 	Fit, Center gravity
    # 1080p 	                        1920 x 1080 Fit, Center gravity

    url = "https://images.igdb.com/igdb/image/upload/t_" + size 

    gameData = igdb_api_get_game_data(request, gameId)
    
    #print("DEBUG: " + gameData)

    url = url+"/" + gameData["cover"]["image_id"] + ".jpg"

    print("DEBUG: " + url)

    return HttpResponse(url) # What Response here?



@login_required(login_url='/app/login')
def sort_games_by(request, value, sort_id):
    categories = Category.objects.all()
    games = Game.objects.filter(deleted=False).order_by(value)
    favorites = Favorite.objects.all()

    args = {}
    args['categories'] = categories
    args['games'] = games
    args['favorites'] = favorites
    args['sort_id'] = sort_id

    return render(request, 'core/index.html', args);


@login_required(login_url='/app/login')
def game_undelete(request, game_id):
    game = Game.objects.get(pk=game_id)
    game.deleted = False
    game.save()

    return HttpResponseRedirect('/app/category/deleted')


@login_required(login_url='/app/login')
def save_game_to_library(request, game_id, user_id):
    game = Game.objects.get(pk=game_id)
    user = User.objects.get(pk=user_id)
    saved_game_instance = SavedGame.objects.get_or_create(user=user, game=game)

    return HttpResponseRedirect('/app')


@login_required(login_url='/app/login')
def saved_games_page(request):
    saved_games = SavedGame.objects.all()
    favorites = Favorite.objects.all()
    categories = Category.objects.all()

    args = {}
    args['saved_games'] = saved_games
    args['favorites'] = favorites
    args['categories'] = categories

    return render(request, 'category/my_library_page.html', args)


@login_required(login_url='/app/login')
def saved_game_details_page(request, saved_game_id):
    game = Game.objects.get(pk=saved_game_id)
    categories = Category.objects.all()
    favorites = Favorite.objects.all()

    args = {}
    args['game'] = game
    args['categories'] = categories
    args['favorites'] = favorites

    return render(request, 'game/saved.html', args)


@login_required(login_url='/app/login')
def delete_game_from_library(request, saved_game_id):
    saved_game = SavedGame.objects.get(pk=saved_game_id)
    saved_game.delete()
    saved_games = SavedGame.objects.all()
    favorites = Favorite.objects.all()
    categories = Category.objects.all()

    args = {}
    args['saved_games'] = saved_games
    args['favorites'] = favorites
    args['categories'] = categories

    return render(request, 'category/my_library_page.html', args)


@login_required(login_url='/app/login')
def category_page(request, category_id):
    categories = Category.objects.all()
    games = Game.objects.filter(category=category_id, deleted=False)
    favorites = Favorite.objects.all();

    args = {}
    args['categories'] = categories
    args['games'] = games
    args['favorites'] = favorites

    return render(request, 'category/page.html', args)


@login_required(login_url='/app/login')
def category_favorites_page(request):
    categories = Category.objects.all()
    games = Game.objects.filter(deleted=False)
    favorites = Favorite.objects.all();

    args = {}
    args['categories'] = categories
    args['games'] = games
    args['favorites'] = favorites

    return render(request, 'category/favorite.html', args)


@login_required(login_url='/app/login')
def category_deleted(request):
    categories = Category.objects.all()
    games = Game.objects.filter(deleted=True)

    args = {}
    args['categories'] = categories
    args['games'] = games

    return render(request, 'category/deleted.html', args)


@login_required(login_url='/app/login')
def category_delete(request, category_id):
    category = Category.objects.get(pk=category_id)
    category.delete()

    categories = Category.objects.all()
    games = Game.objects.all()

    args = {}
    args['categories'] = categories
    args['games'] = games

    return render(request, 'core/index.html', args)


@login_required(login_url='/app/login')
def export_csv(request):
    path = '{}/game_launcher_csv/'.format(os.getcwd())
    exporter = Exporter()

    exporter.export_csv('game.csv', GameResource())
    exporter.export_csv('category.csv', CategoryResource())
    exporter.export_csv('user.csv', UserResource())
    exporter.export_csv('saved_game.csv', SavedGameResource())
    exporter.export_csv('favorite.csv', FavoriteResource())

    csv_files = [os.path.join(path, 'user.csv'), os.path.join(path, 'saved_game.csv'), os.path.join(path, 'favorite.csv'), os.path.join(path, 'game.csv'), os.path.join(path, 'category.csv')]

    zip_obj = zipfile.ZipFile('game_launcher.zip', 'w')
    for csv_file in csv_files:
        zip_obj.write(csv_file, os.path.basename(csv_file))
    zip_obj.close()

    exporter.delete_csv_dir()

    response = HttpResponse(open('game_launcher.zip', 'rb'), content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename="game_launcher.zip"'

    os.remove('{}/game_launcher.zip'.format(os.getcwd()))

    return response


@login_required(login_url='/app/login')
def import_csv(request):
    if request.method == 'POST':
      file = request.FILES['file']
      zip_obj = zipfile.ZipFile(file, 'r')
      csv_files = zip_obj.namelist()
      importer = Importer()

      importer.import_csv_file(zip_obj.read('user.csv').decode(), UserResource())
      importer.import_csv_file(zip_obj.read('category.csv').decode(), CategoryResource())
      importer.import_csv_file(zip_obj.read('game.csv').decode(), GameResource())
      importer.import_csv_file(zip_obj.read('saved_game.csv').decode(), SavedGameResource())
      importer.import_csv_file(zip_obj.read('favorite.csv').decode(), FavoriteResource())

      return HttpResponseRedirect('/app')

    return HttpResponseRedirect('/app')


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

                access_token = igdb_api_authentication(request)
                acto = AccessToken(access_token = access_token)
                acto.save()

                return HttpResponseRedirect('/app')
            else:
                messages.info(request, 'username or password is incorrect')

        context = {}
        return render(request, 'auth/login.html', context)


@login_required(login_url='/app/login')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/app/login')


@login_required(login_url='/app/login')
def mark_game_as_favorite(request, game_id, user_id):
    game = Game.objects.get(pk=game_id)
    user = User.objects.get(pk=user_id)
    favorite_instance = Favorite.objects.get_or_create(user=user, game=game)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/app/login')
def unmark_game_as_favorite(request, game_id, user_id):
    game = Game.objects.get(pk=game_id)
    user = User.objects.get(pk=user_id)
    favorite_instance = Favorite.objects.get(user=user, game=game)
    favorite_instance.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# @csrf_exempt is needed for the registration form to work
# correctly. I do not know as to why, because other forms
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
        return render(request, 'auth/register.html', context)


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


@login_required(login_url='/app/login')
def print_game(request, game_id):
    
    #Create PDF in Folder
    cookies = request.COOKIES
    options = {
    'page-size':'A4',
    'encoding':'utf-8', 
    'margin-top':'0cm',
    'margin-bottom':'0cm',
    'margin-left':'0cm',
    'margin-right':'0cm',
    'dpi':400,
    'cookie' : [('csrftoken',cookies['csrftoken']),('sessionid',cookies["sessionid"])]
}
    url = "http://localhost:8000/app/game/{}".format(game_id) #+ str(game_id)

    #print(url)

    pdfkit.from_url(url, 'media/test3.pdf', options, verbose=True)

    pathpdf = os.getcwd()

    print(pathpdf)

    webbrowser.open("file://"+ pathpdf +"/media/test3.pdf")

    return HttpResponseRedirect('/app')

# For the popups to work, we need to create classes that extend
# the original view (BSModelCreate|Update|DeleteView).
#
# The GameCreateView and CategoryCreateView do work, but the
# update forms do not.
class GameCreateView(BSModalCreateView):
    form_class = GameForm
    template_name = 'game/add.html'
    success_message = 'Success: Game was created.'
    success_url = reverse_lazy('index')


class GameUpdateView(BSModalUpdateView):
    model = Game
    form_class = GameForm
    template_name = 'game/edit.html'
    success_message = 'Success: Game was updated.'
    success_url = reverse_lazy('index')


class GameDeleteView(BSModalDeleteView):
    model = Game
    template_name = 'delete/game.html'
    success_message = 'Success: Game was deleted.'
    success_url = reverse_lazy('index')


class CategoryCreateView(BSModalCreateView):
    form_class = CategoryForm
    template_name = 'category/add.html'
    success_message = 'Success: Category was created.'
    success_url = reverse_lazy('index')


class CategoryUpdateView(BSModalUpdateView):
    model = Category
    template_name = 'category/edit.html'
    form_class = CategoryForm
    success_message = 'Success: Category was updated.'
    success_url = reverse_lazy('index')


class CategoryDeleteView(BSModalDeleteView):
    model = Category
    template_name = 'delete/category.html'
    success_message = 'Success: Category was deleted.'
    success_url = reverse_lazy('index')
