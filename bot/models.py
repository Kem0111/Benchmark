from django.db import models


# Create your models here.
class TelegramUser(models.Model):
    tg_id = models.BigIntegerField(primary_key=True, unique=True,
                                   verbose_name='ID в Телеграм')
    user_name = models.CharField(max_length=150, null=True,
                                 blank=True, verbose_name='Username')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')

    def __str__(self):
        return f"{self.tg_id}"

    class Meta:
        verbose_name = 'Телеграм-пользователя'
        verbose_name_plural = 'Телеграм-пользователи'
        db_table = 'telegram_user'


class Profile(models.Model):
    user = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    industry = models.CharField(max_length=255, verbose_name='Индустрия')
    grade = models.CharField(max_length=100, verbose_name='Класс/Уровень')
    source = models.CharField(max_length=255, verbose_name='Источник')
    contact = models.CharField(max_length=255, verbose_name='Контакт')

    def __str__(self):
        return f"Профайл {self.user.user_name}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
