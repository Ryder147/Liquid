# Generated by Django 4.0.3 on 2022-05-31 17:15

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('developer', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
                ('release_date', models.DateTimeField()),
                ('cover_url', models.CharField(max_length=255)),
                ('stripe_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'games',
            },
        ),
        migrations.CreateModel(
            name='OrderGamesConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='RESTApi.games')),
            ],
            options={
                'db_table': 'order_games_connection',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField()),
                ('pay_time', models.DateTimeField()),
                ('payment_intent_id', models.CharField(blank=True, max_length=255, null=True)),
                ('is_paid', models.SmallIntegerField()),
                ('status', models.TextField(blank=True, null=True)),
                ('user_id', models.IntegerField()),
                ('total_price', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('login', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('date_joined', models.DateTimeField(default=datetime.datetime(2022, 5, 31, 17, 15, 2, 118886, tzinfo=utc))),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('stripe_id', models.CharField(blank=True, max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserLibrary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_games_connection', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='RESTApi.ordergamesconnection')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_library',
            },
        ),
        migrations.CreateModel(
            name='Screens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screen_url', models.CharField(blank=True, max_length=250, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='RESTApi.games')),
            ],
            options={
                'db_table': 'screens',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.CharField(blank=True, max_length=1000, null=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='RESTApi.games')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Requirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('os', models.CharField(max_length=100)),
                ('processor', models.CharField(max_length=100)),
                ('ram', models.CharField(max_length=100)),
                ('graphics_card', models.CharField(max_length=100)),
                ('directx', models.CharField(max_length=100)),
                ('drive_space', models.CharField(max_length=100)),
                ('additional_comments', models.CharField(blank=True, max_length=100, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='RESTApi.games')),
            ],
            options={
                'db_table': 'requirements',
            },
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='RESTApi.games')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ratings',
            },
        ),
        migrations.AddField(
            model_name='ordergamesconnection',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='RESTApi.orders'),
        ),
        migrations.CreateModel(
            name='UsersOrdersConnection',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='RESTApi.orders')),
            ],
            options={
                'db_table': 'users_orders_connection',
                'unique_together': {('user', 'order')},
            },
        ),
    ]