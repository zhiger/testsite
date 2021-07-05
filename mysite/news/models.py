from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Фильм')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_te = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикаций')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновлений')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=False, verbose_name='Фото')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')
    views = models.IntegerField(default=0, verbose_name='Смотрели')

    def get_absolute_url(self):
        """ 'category'- не обходимый маршрут
        kwargs={'category_id': self.pk - построение данного маршрута
        Если вам нужно вернуть абсолютную ссылку, соответствующую указанному представлению, как это делает url,Django предоставляет следующую функцию:
        reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None"""
        return reverse('view_news', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Movies'
        ordering = ['-created_te']
        # ordering = ['pk']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Категория')

    def get_absolute_url(self):
        """ 'category'- не обходимый маршрут
        kwargs={'category_id': self.pk - построение данного маршрута """
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Category'
