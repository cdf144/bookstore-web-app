# Generated by Django 4.2.11 on 2024-04-15 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(default='No description provided'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(default='No description provided'),
        ),
    ]
