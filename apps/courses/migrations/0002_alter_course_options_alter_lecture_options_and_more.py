# Generated by Django 5.0.2 on 2024-02-17 19:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="course",
            options={"verbose_name": "Курс", "verbose_name_plural": "Курсы"},
        ),
        migrations.AlterModelOptions(
            name="lecture",
            options={"verbose_name": "Лекция", "verbose_name_plural": "Лекции"},
        ),
        migrations.AlterModelOptions(
            name="review",
            options={"verbose_name": "Отзыв", "verbose_name_plural": "Отзывы"},
        ),
        migrations.AlterField(
            model_name="course",
            name="image",
            field=models.ImageField(upload_to="courses/", verbose_name="Изображение"),
        ),
        migrations.AlterField(
            model_name="course",
            name="price",
            field=models.DecimalField(
                decimal_places=2, max_digits=6, verbose_name="Цена"
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="rating",
            field=models.FloatField(verbose_name="Рейтинг"),
        ),
        migrations.AlterField(
            model_name="course",
            name="title",
            field=models.CharField(max_length=200, verbose_name="Название"),
        ),
        migrations.AlterField(
            model_name="lecture",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.course",
                verbose_name="Курс",
            ),
        ),
        migrations.AlterField(
            model_name="lecture",
            name="duration",
            field=models.IntegerField(verbose_name="Продолжительность"),
        ),
        migrations.AlterField(
            model_name="lecture",
            name="title",
            field=models.CharField(max_length=200, verbose_name="Название"),
        ),
        migrations.AlterField(
            model_name="review",
            name="comment",
            field=models.TextField(verbose_name="Комментарий"),
        ),
        migrations.AlterField(
            model_name="review",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="courses.course",
                verbose_name="Курс",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
        ),
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.IntegerField(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name="Рейтинг"
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
