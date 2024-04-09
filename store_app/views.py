from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, F, Sum, Case, When, Value, FloatField
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import get_resolver, reverse

from .forms import RegistrationForm, LoginForm
from .models import Games, CustomUser, Wishlist, Cart, PublisherGame, Publisher, SalePublisher

import os
import random


def login_view(request):
    if request.user.is_authenticated:
        return redirect('store_url')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = CustomUser.objects.get(username=username)
            except Exception as e:
                messages.error(request, 'User not Found.')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store_url')
            else:
                messages.error(request, 'Unable to login.')

    form = LoginForm()
    context = {'form': form}
    return render(request, 'store_app/login.html', context)

def registration_view(request):
    if request.user.is_authenticated:
        return redirect('home_url')

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            profile_picture = form.cleaned_data['profile_picture']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            user = CustomUser(username=username, password=password, first_name=first_name, last_name=last_name, email=email)

            if profile_picture: 
                profile_picture_filename = f'{os.path.splitext(profile_picture.name)[0]}_user_{username}{os.path.splitext(profile_picture.name)[1]}'
                upload_to_path = user._meta.get_field('profile_picture').upload_to

                with open(os.path.join(settings.MEDIA_ROOT, upload_to_path, profile_picture_filename), 'wb') as file:
                    for chunk in profile_picture.chunks():
                        file.write(chunk)

                user.profile_picture = os.path.join(upload_to_path, profile_picture_filename)
                file.close()

            user.save()
            messages.success(request, 'Successfully registered!')
            return redirect('login_url')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('registration_url')


    registration_form = RegistrationForm()
    context = {'form': registration_form}
    return render(request, 'store_app/register.html', context)
    
@login_required(login_url='login_url')
def game_view(request, app_id):
    game = get_object_or_404(Games, app_id=app_id)
    categories = game.category.split(',')
    if game.video:
        if ',' in  game.video:
            video = game.video.split(',')[0]
        else:
            video = game.video
    else:
        video = ''

    context = {'game': game, 'categories': categories, 'video': video}
    return render(request, 'store_app/game.html', context)

@login_required(login_url='login_url')
def store_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'logout':
            logout(request)
            return redirect('login_url')

        if action == 'filter_price':
            min_price = request.POST.get('min_price_field')
            max_price = request.POST.get('max_price_field')

            request.session['min_price'] = float(min_price) if min_price != '' else 0
            request.session['max_price'] = float(max_price) if max_price != '' else 0

            return HttpResponseRedirect(reverse('store_url'))

        if action == 'add_to_cart':
            user_id = request.user.id
            game_id = request.POST.get('app_id')

            add_to_cart_game = Cart(game_id=game_id, user_id=user_id)
            add_to_cart_game.save()

        if action == 'add_to_wishlist':
            user_id = request.user.id
            game_id = request.POST.get('app_id')

            wishlist_game = Wishlist(game_id=game_id, user_id=user_id)
            wishlist_game.save()

        if action == 'remove_from_wishlist':
            user_id = request.user.id
            game_id = request.POST.get('app_id')

            remove_game_from_wishlist = Wishlist.objects.filter(game_id=game_id, user_id=user_id)
            remove_game_from_wishlist.delete()


    min_price = request.session.get('min_price', 0)
    max_price = request.session.get('max_price', 999999999)

    store_games = Games.objects.filter(
        price__gte=min_price, price__lte=max_price).order_by(
        '-reviews_positive').values(
        'app_id', 'name', 'price', 'image_main', 'genre', 'windows', 'mac', 'linux')

    wishlisted_games = Wishlist.objects.filter(user_id=request.user).values_list('game_id', flat=True)
    games_in_cart = Cart.objects.filter(user_id=request.user).values_list('game_id', flat=True)

    paginator = Paginator(store_games, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'min_price': min_price,
        'max_price': max_price if max_price != 999999999 else 0,
        'wishlisted_games': wishlisted_games,
        'games_in_cart': games_in_cart,
        'user': request.user
    }
    return render(request, 'store_app/store.html', context)

@login_required(login_url='login_url')
def profile_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_url')

    profile = get_object_or_404(CustomUser, username=request.user)

    total_games_in_cart = Cart.objects.filter(user_id=request.user).count()

    wishlisted_games_ids = Wishlist.objects.filter(user_id=request.user).values_list('game_id', flat=True)
    wishlisted_games = Games.objects.filter(app_id__in=wishlisted_games_ids)

    context = {
                'profile': profile,
                'wishlisted_games': wishlisted_games,
                'total_games_in_cart': total_games_in_cart
    }
    return render(request, 'store_app/profile.html', context)

@login_required(login_url='login_url')
def cart_view(request):
    games_in_cart_ids = Cart.objects.filter(user_id=request.user).values_list('game_id', flat=True)
    games_in_cart = Games.objects.filter(app_id__in=games_in_cart_ids)

    total_price = games_in_cart.aggregate(total_price=Sum('price'))['total_price']

    context = {'games_in_cart': games_in_cart, 'total_price': total_price}
    return render(request, 'store_app/cart.html', context)
def index_view(request):
    resolver = get_resolver()
    patterns = resolver.reverse_dict.keys()

    urls = [(name, resolver.reverse_dict[name][0][0][0]) for name in patterns]

    context = {'urls': urls}
    return render(request, 'store_app/index.html', context)

@login_required(login_url='login_url')
def home_view(request):
    sale_publisher = SalePublisher.objects.annotate(
        game=F('publisher__publishergame__game__name')).annotate(
        price=F('publisher__publishergame__game__price')
    )

    context = {'sale_publisher': sale_publisher}
    return render(request, 'store_app/home.html', context)