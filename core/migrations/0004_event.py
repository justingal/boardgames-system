# Generated by Django 5.2 on 2025-04-15 08:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('address', models.CharField(max_length=255)),
                ('table_size', models.CharField(choices=[('S', 'Mažas'), ('M', 'Vidutinis'), ('L', 'Didelis')], default='M', max_length=1)),
                ('perks', models.TextField(blank=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('visibility', models.CharField(choices=[('public', 'Viešas – visi gali prisijungti'), ('private', 'Privatus – tik pakviestieji')], default='public', max_length=10)),
                ('is_repeating', models.BooleanField(default=False)),
                ('repeat_days', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_created', to=settings.AUTH_USER_MODEL)),
                ('games', models.ManyToManyField(blank=True, related_name='events', to='core.game')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='core.organization')),
                ('players', models.ManyToManyField(blank=True, related_name='events_joined', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
