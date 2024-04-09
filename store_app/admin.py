from django.contrib import admin
from .models import CustomUser, Games, Wishlist, Publisher, PublisherGame, SalePublisher

admin.site.register(CustomUser)
admin.site.register(Games)
admin.site.register(Wishlist)
admin.site.register(Publisher)
admin.site.register(PublisherGame)
admin.site.register(SalePublisher)


