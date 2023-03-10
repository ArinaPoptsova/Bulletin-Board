# Generated by Django 4.1.5 on 2023-01-18 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bulletins', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='response',
            name='bulletin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulletins.bulletin'),
        ),
        migrations.AddField(
            model_name='bulletin',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bulletin',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bulletins.category'),
        ),
    ]
