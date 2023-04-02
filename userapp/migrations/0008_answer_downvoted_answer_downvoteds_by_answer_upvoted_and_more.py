# Generated by Django 4.0.5 on 2023-03-10 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0007_question_downvoted_by_question_upvoted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='downvoted',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answer',
            name='downvoteds_by',
            field=models.ManyToManyField(blank=True, related_name='downvoted_answers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='upvoted',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answer',
            name='upvoteds_by',
            field=models.ManyToManyField(blank=True, related_name='upvoted_answers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='downvoted_by',
            field=models.ManyToManyField(blank=True, related_name='downvoted_questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='upvoted_by',
            field=models.ManyToManyField(blank=True, related_name='upvoted_questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL),
        ),
    ]
