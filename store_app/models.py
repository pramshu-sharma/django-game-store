from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    profile_picture = models.ImageField(upload_to='images', blank=True)


class Games(models.Model):
    app_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=500, null=True)
    release_date = models.DateField(null=True)
    required_age = models.PositiveSmallIntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    dlc_count = models.IntegerField(null=True)
    description_long = models.TextField(null=True)
    description_short = models.TextField(null=True)
    image_main = models.URLField(null=True)
    website = models.URLField(null=True)
    windows = models.BooleanField(default=False)
    mac = models.BooleanField(default=False)
    linux = models.BooleanField(default=False)
    metacritic_score = models.SmallIntegerField(default=None)
    metacritic_url = models.URLField(null=True)
    achievements = models.PositiveIntegerField(null=True)
    recommendations = models.IntegerField(null=True)
    user_score = models.FloatField(default=None)
    reviews_positive = models.IntegerField(null=True)
    reviews_negative = models.IntegerField(null=True)
    reviews_ratio_p_to_n = models.FloatField(default=None)
    peak_player_count = models.IntegerField(null=True)
    screenshot = models.TextField(null=True)
    genre = models.TextField(null=True)
    developer = models.TextField(null=True)
    video = models.TextField(null=True)
    category = models.TextField(null=True)
    tags = models.TextField(null=True)
    create_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE, to_field='app_id')
    create_ts = models.DateTimeField(auto_now_add=True, blank=True)
    update_ts = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return self.user


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE, to_field='app_id')
    create_ts = models.DateTimeField(auto_now_add=True, blank=True)
    update_ts = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return str(self.user)


class Publisher(models.Model):
    publisher = models.CharField(max_length=200)
    create_ts = models.DateTimeField(auto_now_add=True, blank=True)
    update_ts = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.publisher


class PublisherGame(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('publisher', 'game')

    def __str__(self):
        return f'{self.publisher}_{self.game}'


class SalePublisher(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    sale_percent = models.DecimalField(max_digits=4, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    create_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(sale_percent__gt=0) & Q(sale_percent__lt=1),
                name='check_publisher_sale_percent'
            )
        ]

    def __str__(self):
        return self.publisher.publisher

    def check_if_sale_active(self):
        now = timezone.now().date()
        active_sale_exists = SalePublisher.objects.filter(
            publisher=self.publisher,
            start_date__lte=now,
            end_date__gte=now
        ).exists()

        if active_sale_exists:
            raise ValidationError('Sale for the publisher is already active.')

    def clean(self):
        self.check_if_sale_active()


