# Generated by Django 5.1.1 on 2024-11-14 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_slot',
            field=models.IntegerField(default=20),
        ),
    ]