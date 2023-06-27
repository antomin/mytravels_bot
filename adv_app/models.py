from django.db import models


class AdvPhoto(models.Model):
    title = models.CharField(verbose_name='название', max_length=100)
    url = models.ImageField(verbose_name='изображение', upload_to='adv_images')

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return self.title


class AdvButton(models.Model):
    title = models.CharField(verbose_name='текст кнопки', max_length=100)
    url = models.URLField(verbose_name='ссылка')

    class Meta:
        verbose_name = 'кнопка'
        verbose_name_plural = 'кнопки'

    def __str__(self):
        return self.title


class Adv(models.Model):
    title = models.CharField(verbose_name='название кампании', max_length=100, unique=True)
    text = models.TextField(verbose_name='текст')
    time_exec = models.DateTimeField(verbose_name='время запуска')
    enabled = models.BooleanField(verbose_name='включена', default=False)
    photos = models.ManyToManyField(AdvPhoto, verbose_name='вложенные изображения', blank=True)
    buttons = models.ManyToManyField(AdvButton, verbose_name='кнопки', blank=True)

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def __str__(self):
        return self.title
