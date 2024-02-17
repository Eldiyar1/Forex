from django.db import models
from apps.users.models import User


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(upload_to='courses/', verbose_name='Изображение')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures', verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название')
    duration = models.IntegerField(verbose_name='Продолжительность')
    video_url = models.URLField(verbose_name='Ссылка на видео')

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'

    def __str__(self):
        return self.title


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews', verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='reviews', verbose_name='Пользователь')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Рейтинг')
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('course', 'user')

    def __str__(self):
        return f"Review for {self.course.title} - Rating: {self.rating}"
