# Generated by Django 3.0.8 on 2020-07-14 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='user',
        ),
        migrations.AddField(
            model_name='class',
            name='added_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='class',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='class',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]