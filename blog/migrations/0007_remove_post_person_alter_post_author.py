# Generated by Django 4.0.3 on 2022-03-22 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='person',
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
