# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from typing import List
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser

class Games(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100) 
    cover_url = models.CharField(max_length=255)
    stripe_id = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    description = models.CharField(max_length=800)
    class Meta:
        db_table = 'games'


class OrderGamesConnection(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    game = models.ForeignKey(Games, models.DO_NOTHING)

    class Meta:
        db_table = 'order_games_connection'


class Orders(models.Model):
    create_time = models.DateTimeField()
    pay_time = models.DateTimeField(null=True)
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField()
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_id = models.IntegerField()
    total_price = models.TextField(blank=True, null=True)  # This field type is a guess.
    checkout_session_id = models.CharField(max_length=255)
    class Meta:
        db_table = 'orders'


class Ratings(models.Model):
    game = models.ForeignKey(Games, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    value = models.IntegerField()
    class Meta:
        db_table = 'ratings'


class Requirements(models.Model):
    os = models.CharField(max_length=100)
    processor = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    graphics_card = models.CharField(max_length=100)
    directx = models.CharField(max_length=100)
    drive_space = models.CharField(max_length=100)
    additional_comments = models.CharField(max_length=100, blank=True, null=True)
    game = models.ForeignKey(Games, models.DO_NOTHING,related_name='requirements')

    class Meta:
        db_table = 'requirements'


class Reviews(models.Model):
    review_text = models.CharField(max_length=1000, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    game = models.ForeignKey(Games, models.DO_NOTHING, related_name='game_reviews')
    user = models.ForeignKey('User', models.DO_NOTHING, related_name='user')

    class Meta:
        db_table = 'reviews'


class Screens(models.Model):
    screen_url = models.CharField(max_length=250, blank=True, null=True)
    game = models.ForeignKey(Games, models.DO_NOTHING, related_name='screens')

    class Meta:
        db_table = 'screens'


class UserLibrary(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING)
    game = models.ForeignKey(Games, models.DO_NOTHING)

    class Meta:
        db_table = 'user_library'


class User(AbstractUser):
    login = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=250)
    email = models.CharField(unique=True, max_length=50)
    date_joined = models.DateTimeField(default=timezone.now())
    last_login = models.DateTimeField(blank=True, null=True)
    stripe_id = models.CharField(max_length=255, blank=True, null=True)
    username = None

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = []

    class Meta:
        db_table = 'users'


class UsersOrdersConnection(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    order = models.ForeignKey(Orders, models.DO_NOTHING)

    class Meta:
        db_table = 'users_orders_connection'
        unique_together = (('user', 'order'),)

class Cart(models.Model):
    game = models.ForeignKey('Games', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        db_table = 'cart'