# Generated by Django 4.0.2 on 2022-03-07 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=256, verbose_name='access_token')),
            ],
        ),
        migrations.AlterField(
            model_name='game',
            name='developer',
            field=models.ForeignKey(limit_choices_to={'is_developer': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Entwickler'),
        ),
        migrations.AlterField(
            model_name='game',
            name='publisher',
            field=models.ForeignKey(limit_choices_to={'is_publisher': True}, on_delete=django.db.models.deletion.CASCADE, related_name='publisher', to=settings.AUTH_USER_MODEL, verbose_name='Herausgeber'),
        ),
    ]