from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Почта', unique=True)
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mail(models.Model):
    mail_theme = models.CharField(max_length=150, verbose_name='Тема')
    mail_body = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return self.mail_theme

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'


class Mailing(models.Model):
    period_choice = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    period = models.CharField(max_length=10, choices=period_choice, verbose_name='Периодичность')
    starting_at = models.DateTimeField(verbose_name='время и дата начала рассылки')
    ending_at = models.DateTimeField(verbose_name='время и дата окончания рассылки')
    last_mailing_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время и дата последней рассылки',
                                                 null=True, blank=True)
    next_mailing_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время и дата следующей рассылки',
                                                 null=True, blank=True)
    mailing_status = models.CharField(max_length=20, verbose_name='Статус рассылки', default='Создана')
    mail = models.ForeignKey(Mail, on_delete=models.SET_NULL, null=True, blank=True)
    clients = models.ManyToManyField(Client)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Рассылка с {self.starting_at} по {self.ending_at}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Log(models.Model):
    last_mailing_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время и дата последней рассылки',
                                                 null=True, blank=True)
    status = models.CharField(max_length=20, verbose_name='Статус попытки')
    mail_server_callback = models.TextField(verbose_name='Ответ почтового сервера, если он был')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f'Лог - {self.status}'

    def save(self, *args, **kwargs):
        if self.mailing:
            self.last_mailing_datetime = self.mailing.last_mailing_datetime
        super(Log, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
