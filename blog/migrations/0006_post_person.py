# Generated by Django 4.0.3 on 2022-03-17 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='person',
            field=models.CharField(default=1, max_length=40),
        ),
    ]
