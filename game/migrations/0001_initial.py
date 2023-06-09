# Generated by Django 3.2.18 on 2023-04-04 06:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('developer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('publication_date', models.DateField(default=datetime.date.today)),
                ('status', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='developer.developer')),
            ],
        ),
    ]
