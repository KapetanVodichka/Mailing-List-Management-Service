from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    period_choice = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    period = models.CharField(max_length=10, choices=period_choice, verbose_name='Периодичность')
    # mailing_time = models.TimeField(auto_now_add=True, verbose_name='Время рассылки')
    starting_at = models.TimeField(verbose_name='время начала рассылки')
    ending_at = models.TimeField(verbose_name='время окончания рассылки')
    mailing_status = models.CharField(max_length=20, verbose_name='Статус рассылки')

    def __str__(self):
        return f'Рассылка с {self.starting_at} по {self.ending_at}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Почта', unique=True)
    comment = models.TextField(verbose_name='Комментарий')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

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


class Log(models.Model):
    last_try_time = models.DateTimeField(verbose_name='Дата и время последней рассылки')
    status = models.CharField(max_length=20, verbose_name='Статус попытки')
    mail_server_callback = models.TextField(verbose_name='Ответ почтового сервера, если он был')

    def __str__(self):
        return f'Лог - {self.status}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'