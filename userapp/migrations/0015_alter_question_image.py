# Generated by Django 4.0.5 on 2023-03-21 16:42

from django.db import migrations, models
import userapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0014_tag_remove_question_tags_question_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=userapp.models.upload_to),
        ),
    ]
