from django.db import models

from tgbot_app.models import Profile


class Order(models.Model):
    user = models.ForeignKey(to=Profile, verbose_name='пользователь', on_delete=models.CASCADE)
    prev_order = models.ForeignKey(to='self', verbose_name='предыдущий счёт', null=True, blank=True,
                                   on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='сумма')
    is_paid = models.BooleanField(verbose_name='оплачен', default=False)
    created_at = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='последнее обновление', auto_now=True)

    class Meta:
        verbose_name = 'счёт'
        verbose_name_plural = 'счета'
        ordering = ('created_at', )

    def __str__(self):
        return f'{self.id} | {self.user.tgid}'

