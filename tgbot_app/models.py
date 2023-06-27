from django.db import models


class Profile(models.Model):
    tgid = models.BigIntegerField(verbose_name='телеграм ID', primary_key=True, db_index=True)
    first_name = models.CharField(verbose_name='имя', max_length=100, blank=True, null=True)
    last_name = models.CharField(verbose_name='фамилия', max_length=100, blank=True, null=True)
    username = models.CharField(verbose_name='имя пользователя', max_length=100, blank=True, null=True)
    is_admin = models.BooleanField(verbose_name='администратор', default=False)
    is_active = models.BooleanField(verbose_name='активен', default=True)
    created_at = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='последнее обновление', auto_now=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.tgid


class Country(models.Model):
    code = models.CharField(verbose_name='код', max_length=4, primary_key=True, db_index=True)
    title = models.CharField(verbose_name='название', max_length=100)

    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'
        ordering = ('title', )

    def __str__(self):
        return f'{self.title}({self.code})'


class City(models.Model):
    code = models.CharField(verbose_name='код', max_length=4, primary_key=True, db_index=True)
    title = models.CharField(verbose_name='название', max_length=100)
    country = models.ForeignKey(to=Country, verbose_name='страна', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'
        ordering = ('title', )

    def __str__(self):
        return f'{self.title}({self.code}) | {self.country.title}'


class Airport(models.Model):
    code = models.CharField(verbose_name='код', max_length=4, primary_key=True, db_index=True)
    title = models.CharField(verbose_name='название', max_length=100)

    class Meta:
        verbose_name = 'аэропорт'
        verbose_name_plural = 'аэропорты'

    def __str__(self):
        return f'{self.title}({self.code})'


class Airline(models.Model):
    code = models.CharField(verbose_name='код', max_length=4, primary_key=True, db_index=True)
    title = models.CharField(verbose_name='название', max_length=100)

    class Meta:
        verbose_name = 'авиакомпания'
        verbose_name_plural = 'авиакомпании'

    def __str__(self):
        return f'{self.title}({self.code})'
