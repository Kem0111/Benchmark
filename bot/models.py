from django.db import models


# Create your models here.
class TelegramUser(models.Model):
    tg_id = models.BigIntegerField(primary_key=True, unique=True,
                                   verbose_name='ID в Телеграм')
    user_name = models.CharField(max_length=150, null=True,
                                 blank=True, verbose_name='Username')

    def __str__(self):
        return f"{self.tg_id}"

    class Meta:
        verbose_name = 'Телеграм-пользователя'
        verbose_name_plural = 'Телеграм-пользователи'
        db_table = 'telegram_user'
