import datetime
import os
import random
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.aggregates import StringAgg
from django.core.paginator import Paginator
from django.db.models import Q, F, Sum, Case, When, Value, FloatField, CharField, Count
from django.db.models.functions import Concat, Substr, Upper
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import get_resolver, reverse

from .forms import RegistrationForm, LoginForm
from .models import (
    Games, CustomUser, Wishlist, Cart, PublisherGame, Publisher,
    SalePublisher, Genre, GenreGame, Reviews, EditReviewTest
)


def flush_store_filter_session_variables(request):
    keys = ['selected_genres', 'selected_platforms', 'selected_prices', 'selected_publisher']

    for key in keys:
        if key in request.session:
            del request.session[key]
def login_view(request): # needs to check incorrect username and password
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

    context = {
        'form': LoginForm()
    }
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

    context = {
        'form': RegistrationForm()
    }
    return render(request, 'store_app/register.html', context)
    
@login_required(login_url='login_url')
def game_view(request, app_id):
    # check csrf token in JS
    flush_store_filter_session_variables(request)

    if request.method == 'POST':
        action = request.POST['action']

        if action == 'save-user-review':
            print(request.POST)

        if action == 'post-review':
            review = request.POST['review-textarea']

            if len(review) >= 10001:
                messages.error(request, 'Review length is too long.')
                return redirect('game_url', app_id=app_id)

            game = Games.objects.get(app_id=app_id)
            user = request.user

            review = Reviews(user=user, game=game, review=review)
            review.save()
            messages.success(request, 'Review saved successfully.')
            return redirect('game_url', app_id=app_id)

    game = get_object_or_404(Games, app_id=app_id)
    video = None
    if game.video:
        video = game.video.split(',')[0] if ',' in  game.video else game.video

    reviews = Reviews.objects.filter(game=game.id)
    user_review = None

    try:
        user_review = get_object_or_404(Reviews, user=request.user)
        reviews = reviews.exclude(user=request.user)
    except Exception:
        pass

    context = {
        'game': game,
        'reviews': reviews,
        'user_review': user_review,
        'categories': game.category.split(','),
        'video': video
    }
    return render(request, 'store_app/game.html', context)

@login_required(login_url='login_url')
def store_view(request):
    if 'publisher' in request.GET:
        if request.GET['publisher'] == 'all':
            del request.session['selected_publisher']
        else:
            request.session['selected_publisher'] = request.GET['publisher']

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'logout':
            logout(request)
            return redirect('login_url')

        if action == 'filter_store':
            request.session['selected_genres'] = request.POST.getlist('genre-checkbox')
            request.session['selected_platforms'] = request.POST.getlist('platform-checkbox[]')

            request.session['min_price'], request.session['max_price'] = '', ''
            previous_min_price, previous_max_price = '', ''
            request_min_price, request_max_price = request.POST.get('min_price_field'), request.POST.get(
                'max_price_field')

            if (request_min_price != '' and request_min_price != previous_min_price) and (
                    request_max_price != '' and request_max_price != previous_max_price):
                request.session['selected_prices'] = (request_min_price, request_max_price)

            previous_min_price, previous_max_price = request.session['min_price'], request.session['max_price']

            return HttpResponseRedirect(reverse('store_url'))

        if action == 'clear_filter_store':
            keys_to_flush = ['selected_genres', 'selected_platforms', 'selected_prices']

            for key in list(request.session.keys()):
                if key in keys_to_flush:
                    del request.session[key]

            return HttpResponseRedirect(reverse('store_url'))

        if action == 'add_to_cart':
            user_id = request.user.id
            game_id = request.POST.get('app_id')

            add_to_cart_game = Cart(game_id=game_id, user_id=user_id)
            add_to_cart_game.save()

        if action == 'remove_from_cart':
            user_id = request.user.id
            game_id = request.POST.get('app_id')

            remove_from_cart_game = Cart.objects.filter(game_id=game_id, user_id=user_id)
            remove_from_cart_game.delete()

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

    store_games = Games.objects.values(
        'app_id', 'name', 'price', 'sale_price', 'image_main', 'windows', 'mac', 'linux').annotate(
        genres_all=StringAgg(
            F('genregame__genre__genre'),
            delimiter=', '
        )
    ).order_by(
        '-peak_player_count')

    publishers = Publisher.objects.annotate(
        game_count=Count('publishergame__game')
    ).values('id', 'publisher', 'game_count').order_by('-game_count')[:5]

    if 'selected_prices' in request.session and request.session['selected_prices'] is not None:
        min_price, max_price = request.session['selected_prices'][0], request.session['selected_prices'][1]

        if min_price and max_price:
            min_price, max_price = float(min_price), float(max_price)
            store_games = store_games.filter(price__gte=min_price, price__lte=max_price).order_by('name')

    if 'selected_genres' in request.session and request.session['selected_genres'] is not None:
        query_genre = Q()
        for genre in request.session['selected_genres']:
            q_object = Q(**{'genres_all__icontains': genre})
            query_genre &= q_object

        store_games = store_games.filter(query_genre)

    if 'selected_platforms' in request.session and request.session['selected_platforms'] is not None:
        query_platform = Q()
        for platform in request.session['selected_platforms']:
            q_object = Q(**{platform: 1})
            query_platform &= q_object

        store_games = store_games.filter(query_platform).order_by('name')

    if 'selected_publisher' in request.session and request.session['selected_publisher'] is not None:
        selected_publisher = request.session['selected_publisher']

        store_games = store_games.filter(publishergame__publisher__publisher=selected_publisher).order_by('name')

    wishlisted_games = Wishlist.objects.filter(user_id=request.user).values_list('game_id', flat=True)
    games_in_cart = Cart.objects.filter(user_id=request.user).values_list('game_id', flat=True)
    genres = Genre.objects.values_list('genre', flat=True)

    paginator = Paginator(store_games, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'genres': genres,
        'wishlisted_games': wishlisted_games,
        'games_in_cart': games_in_cart,
        'user': request.user,
        'publishers': publishers,
    }

    return render(request, 'store_app/store.html', context)

@login_required(login_url='login_url')
def profile_view(request):
    flush_store_filter_session_variables(request)

    if request.method == 'POST':
        logout(request)
        return redirect('login_url')

    wishlisted_games_ids = Wishlist.objects.filter(user_id=request.user).values_list('game_id', flat=True)

    context = {
                'profile': get_object_or_404(CustomUser, username=request.user),
                'wishlisted_games': Games.objects.filter(app_id__in=wishlisted_games_ids),
                'total_games_in_cart': Cart.objects.filter(user_id=request.user).count()
    }
    return render(request, 'store_app/profile.html', context)

@login_required(login_url='login_url')
def cart_view(request):
    games_in_cart_ids = Cart.objects.filter(user_id=request.user).values_list('game_id', flat=True)
    games_in_cart = Games.objects.filter(app_id__in=games_in_cart_ids)

    total_price = games_in_cart.aggregate(total_price=Sum('price'))['total_price']

    context = {'games_in_cart': games_in_cart, 'total_price': total_price}
    return render(request, 'store_app/cart.html', context)

@login_required(login_url='login_url')
def index_view(request):
    today = datetime.datetime.now().date()

    if request.user.is_superuser:
        resolver = get_resolver()
        patterns = resolver.reverse_dict.keys()
        urls = [(name, resolver.reverse_dict[name][0][0][0]) for name in patterns]

        context = {
            'urls': urls
        }

        if request.method == 'POST':
            action = request.POST.get('action')

            if action == 'set-sale-prices': # logic needs to inquire for games that were on sale but now are not
                games_on_sale = SalePublisher.objects.annotate(
                    game_id=F('publisher__publishergame__game')).filter(
                    start_date__lte=today, end_date__gte=today
                    ).values(
                    'game_id', 'sale_percent')

                for sale_info in games_on_sale:
                    game_id = sale_info['game_id']
                    sale_percent = sale_info['sale_percent']

                    game = Games.objects.get(id=game_id)

                    if game.price != 0:
                        new_sale_price = round(game.price - game.price * sale_percent, 2)
                        game.sale_price = new_sale_price
                        game.save()

                games_on_sale_ids = games_on_sale.values('game_id')
                Games.objects.exclude(id__in=games_on_sale_ids).update(sale_price=0)

                context['games_on_sale'] = len(games_on_sale_ids)
                return render(request, 'store_app/index.html', context)

        return render(request, 'store_app/index.html', context)
    else:
        return redirect('store_url')

def publishers_view(request):
    numbered_first_letters = ['0', '1', '2', '3', '4' , '5', '6', '7', '8', '9']

    publishers = Publisher.objects.annotate(
        first_letter=Upper(Substr('publisher', 1, 1))).annotate(
        publisher_first_letter=
        Case(
            When(first_letter__in=numbered_first_letters, then=Value('0 - 9')),
                    default=F('first_letter'),
                    output_field=CharField()
        )
    ).order_by('publisher_first_letter')

    publishers = publishers.annotate(game_count=Count('publishergame__game')).order_by('publisher')

    context = {
        'publishers': publishers
    }
    return render(request, 'store_app/publishers.html', context)

def test_view(request):
    # cannot edit review after JS POST request
    if request.method == 'POST':
        try:
            post_review = json.loads(request.body.decode('utf-8'))
            new_review = get_object_or_404(EditReviewTest, id=post_review['id'])
            new_review.review = post_review['review'].strip()
            new_review.save()
            return JsonResponse({'message': 'review posted'}, status=200)
        except json.JSONDecodeError:
            return  JsonResponse({'message': 'Something went wrong'}, status=400)

    reviews = EditReviewTest.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'store_app/test.html', context)
