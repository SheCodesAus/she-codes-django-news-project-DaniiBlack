# Generated by Django 4.1.3 on 2022-12-18 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_remove_newsstory_liked_by_newsstory_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsstory',
            name='categories',
            field=models.CharField(choices=[('clickbait', 'Clickbait'), ('politics', 'Politics'), ('travel', 'Travel'), ('badbitch', 'Bad bitch, its a genre')], default='Clickbait', max_length=20),
        ),
    ]
