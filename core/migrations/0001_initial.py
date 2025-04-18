# Generated by Django 5.2 on 2025-04-09 16:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bgg_id', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=255)),
                ('min_players', models.IntegerField(blank=True, null=True)),
                ('max_players', models.IntegerField(blank=True, null=True)),
                ('playtime_minutes', models.IntegerField(blank=True, null=True)),
                ('thumbnail_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('privacy', models.CharField(choices=[('public', 'Vieša'), ('protected', 'Pusiau privati'), ('private', 'Privati')], default='public', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(blank=True, to='core.gamecategory')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizations_created', to=settings.AUTH_USER_MODEL)),
                ('games', models.ManyToManyField(blank=True, to='core.game')),
                ('members', models.ManyToManyField(blank=True, related_name='organizations_joined', through='core.Membership', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='core.organization'),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('user', 'organization')},
        ),
        migrations.CreateModel(
            name='UserGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'game')},
            },
        ),
    ]
