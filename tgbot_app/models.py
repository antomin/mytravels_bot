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
        return f'{self.tgid} | {self.username}'


class AviaCountry(models.Model):
    code = models.CharField(verbose_name='код', max_length=4, primary_key=True, db_index=True)
    title = models.CharField(verbose_name='название', max_length=100)
    priority = models.IntegerField(verbose_name='приоритет', default=300)

    class Meta:
        verbose_name = 'страна авиасейлс'
        verbose_name_plural = 'страны авиасейлс'
        ordering = ('priority', 'title', )

    def __str__(self):
        return f'{self.title}({self.code})'


class AviaCity(models.Model):
    code = models.CharField(verbose_name='код', max_length=4, primary_key=True, db_index=True)
    title = models.CharField(verbose_name='название', max_length=100)
    country = models.ForeignKey(to=AviaCountry, verbose_name='страна', on_delete=models.CASCADE)
    priority = models.IntegerField(verbose_name='приоритет', default=300)

    class Meta:
        verbose_name = 'город авиасейлс'
        verbose_name_plural = 'города авиасейлс'
        ordering = ('priority', 'title', )

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


class ExcursionCountry(models.Model):
    id = models.IntegerField(verbose_name='ID', primary_key=True, db_index=True)
    title = models.CharField(verbose_name='название', max_length=100)
    priority = models.IntegerField(verbose_name='приоритет', default=300)

    class Meta:
        verbose_name = 'страна экскурсии'
        verbose_name_plural = 'страны экскурсии'
        ordering = ('id', )

    def __str__(self):
        return f'{self.title}({self.id})'


class ExcursionCity(models.Model):
    id = models.IntegerField(verbose_name='ID', primary_key=True, db_index=True)
    title = models.CharField(verbose_name='название', max_length=100)
    country = models.ForeignKey(to=ExcursionCountry, verbose_name='страна', on_delete=models.CASCADE)
    priority = models.IntegerField(verbose_name='приоритет', default=300)

    class Meta:
        verbose_name = 'страна экскурсии'
        verbose_name_plural = 'страны экскурсии'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title}({self.id})'


class FlightSubscription(models.Model):
    user = models.ForeignKey(Profile, verbose_name='пользователь', on_delete=models.CASCADE)
    depart_city = models.ForeignKey(AviaCity, verbose_name='город отправления', related_name='subscription_depart_city',
                                    on_delete=models.CASCADE)
    arrival_city = models.ForeignKey(AviaCity, verbose_name='город прибытия', related_name='subscription_arrival_city',
                                     on_delete=models.CASCADE)
    depart_date = models.DateField(verbose_name='дата отправления')
    return_date = models.DateField(verbose_name='дата возвращения', blank=True, null=True)
    is_direct = models.BooleanField(verbose_name='без пересадок')
    last_price = models.IntegerField(verbose_name='последняя цена')

    class Meta:
        verbose_name = 'подписка на билет'
        verbose_name_plural = 'подписки на билеты'

    def __str__(self):
        return f'{self.user.tgid} | {self.depart_city.title} - {self.arrival_city.title} | {self.depart_date}'
