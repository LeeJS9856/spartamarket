# Generated by Django 4.2 on 2024-04-17 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_article_like_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]