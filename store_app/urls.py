from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index_url'),
    path('login/', views.login_view, name='login_url'),
    path('game/<int:app_id>', views.game_view, name='game_url'),
    path('store/', views.store_view, name='store_url'),
    path('register/', views.registration_view, name='registration_url'),
    path('profile/', views.profile_view, name='profile_url'),
    path('cart/', views.cart_view, name='cart_url'),
    path('test/', views.test_view, name='test_url')
]