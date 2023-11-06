from datetime import datetime, timedelta
from django.utils import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, Log


def daily_mailing():
    # Получаем текущее время
    current_time = datetime.now()

    print(f"Задача 'daily_mailing' запущена в {current_time}")

    # Получаем активные рассылки, которые должны быть отправлены в данный момент
    active_mailings = Mailing.objects.filter(starting_at__lte=current_time, ending_at__gte=current_time,
                                             mailing_status__in=['Создана', 'Запущена'], period='daily',
                                             next_mailing_datetime__lte=current_time)

    for mailing in active_mailings:
        # Обновляем статус рассылки на "Запущена"
        mailing.mailing_status = 'Запущена'
        mailing.save()
        print('Обновили статус рассылки - запущена')

        # Получаем клиентов, которые должны получить это сообщение
        clients = mailing.clients.all()
        print('Взяли клиентов')

        for client in clients:
            # Извлекаем theme и body из объекта Mail
            mail_theme = mailing.mail.mail_theme
            mail_body = mailing.mail.mail_body
            print('Извлекли Mail')

            try:
                # Отправляем письмо
                send_mail(mail_theme, mail_body, EMAIL_HOST_USER, [client.email])
                print('вроде как отправили письмо')

                # Обновляем лог рассылки
                log = Log(mailing=mailing, last_mailing_datetime=datetime.now(), status='Отправлено',
                          mail_server_callback='Успешно отправлено')
                log.save()

            except Exception as e:
                # Обработка ошибок
                log = Log(mailing=mailing, last_mailing_datetime=datetime.now(), status='Ошибка', mail_server_callback=str(e))
                log.save()
                print(f'ошибка {e}')

        # Обновляем статус рассылки на "Завершена", если это последняя рассылка
        mailing.last_mailing_datetime = current_time
        mailing.next_mailing_datetime = mailing.last_mailing_datetime + timedelta(days=1)
        mailing.save()

        target_timezone = timezone.get_current_timezone()
        next_mailing_datetime = mailing.next_mailing_datetime.astimezone(target_timezone)

        if next_mailing_datetime > mailing.ending_at:
            mailing.mailing_status = 'Завершена'
            mailing.save()


def weekly_mailing():
    # Получаем текущее время
    current_time = datetime.now()

    print(f"Задача 'weekly_mailing' запущена в {current_time}")

    # Получаем активные рассылки, которые должны быть отправлены в данный момент
    active_mailings = Mailing.objects.filter(starting_at__lte=current_time, ending_at__gte=current_time,
                                             mailing_status__in=['Создана', 'Запущена'], period='weekly',
                                             next_mailing_datetime__lte=current_time)

    for mailing in active_mailings:
        # Обновляем статус рассылки на "Запущена"
        mailing.mailing_status = 'Запущена'
        mailing.save()
        print('Обновили статус рассылки - запущена')

        # Получаем клиентов, которые должны получить это сообщение
        clients = mailing.clients.all()
        print('Взяли клиентов')

        for client in clients:
            # Извлекаем theme и body из объекта Mail
            mail_theme = mailing.mail.mail_theme
            mail_body = mailing.mail.mail_body
            print('Извлекли Mail')

            try:
                # Отправляем письмо
                send_mail(mail_theme, mail_body, EMAIL_HOST_USER, [client.email])
                print('вроде как отправили письмо')

                # Обновляем лог рассылки
                log = Log(mailing=mailing, last_mailing_datetime=datetime.now(), status='Отправлено',
                          mail_server_callback='Успешно отправлено')
                log.save()

            except Exception as e:
                # Обработка ошибок
                log = Log(mailing=mailing, last_mailing_datetime=datetime.now(), status='Ошибка', mail_server_callback=str(e))
                log.save()
                print(f'ошибка {e}')

        # Обновляем статус рассылки на "Завершена", если это последняя рассылка
        mailing.last_mailing_datetime = current_time
        mailing.next_mailing_datetime = mailing.last_mailing_datetime + timedelta(weeks=1)
        mailing.save()

        target_timezone = timezone.get_current_timezone()
        next_mailing_datetime = mailing.next_mailing_datetime.astimezone(target_timezone)

        if next_mailing_datetime > mailing.ending_at:
            mailing.mailing_status = 'Завершена'
            mailing.save()


def monthly_mailing():
    # Получаем текущее время
    current_time = datetime.now()

    print(f"Задача 'monthly_mailing' запущена в {current_time}")

    # Получаем активные рассылки, которые должны быть отправлены в данный момент
    active_mailings = Mailing.objects.filter(starting_at__lte=current_time, ending_at__gte=current_time,
                                             mailing_status__in=['Создана', 'Запущена'], period='monthly',
                                             next_mailing_datetime__lte=current_time)

    for mailing in active_mailings:
        # Обновляем статус рассылки на "Запущена"
        mailing.mailing_status = 'Запущена'
        mailing.save()
        print('Обновили статус рассылки - запущена')

        # Получаем клиентов, которые должны получить это сообщение
        clients = mailing.clients.all()
        print('Взяли клиентов')

        for client in clients:
            # Извлекаем theme и body из объекта Mail
            mail_theme = mailing.mail.mail_theme
            mail_body = mailing.mail.mail_body
            print('Извлекли Mail')

            try:
                # Отправляем письмо
                send_mail(mail_theme, mail_body, EMAIL_HOST_USER, [client.email])
                print('вроде как отправили письмо')

                # Обновляем лог рассылки
                log = Log(mailing=mailing, last_mailing_datetime=datetime.now(), status='Отправлено',
                          mail_server_callback='Успешно отправлено')
                log.save()

            except Exception as e:
                # Обработка ошибок
                log = Log(mailing=mailing, last_mailing_datetime=datetime.now(), status='Ошибка', mail_server_callback=str(e))
                log.save()
                print(f'ошибка {e}')

        # Обновляем статус рассылки на "Завершена", если это последняя рассылка
        mailing.last_mailing_datetime = current_time
        mailing.next_mailing_datetime = mailing.last_mailing_datetime + timedelta(days=30)
        mailing.save()

        target_timezone = timezone.get_current_timezone()
        next_mailing_datetime = mailing.next_mailing_datetime.astimezone(target_timezone)

        if next_mailing_datetime > mailing.ending_at:
            mailing.mailing_status = 'Завершена'
            mailing.save()


@util.close_old_connections
def delete_old_job_executions(max_age=604800):
    """
    Эта задача удаляет записи об исполнении задач APScheduler старше `max_age` из базы данных.
    Это помогает предотвратить переполнение базы данных старыми записями, которые больше не актуальны.

    :param max_age: Максимальный период времени для сохранения записей об исполнении задач.
                    По умолчанию - 7 дней.
    """
    print("Задача 'delete_old_job_executions' запущена")
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Запускает APScheduler."

    def handle(self, *args, **options):

        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            daily_mailing,
            trigger=CronTrigger(second="*/30"),  # Запускать каждые 30 секунд
            id="daily",
            max_instances=1,
            replace_existing=True,
        )
        print("Добавлена задача 'daily_mailing'.")

        scheduler.add_job(
            weekly_mailing,
            trigger=CronTrigger(minute="*/15"),  # Запускать каждые 15 минут
            id="weekly",
            max_instances=1,
            replace_existing=True,
        )
        print("Добавлена задача 'weekly_mailing'.")

        scheduler.add_job(
            monthly_mailing,
            trigger=CronTrigger(hour="*/1"),  # Запускать каждый час
            id="monthly",
            max_instances=1,
            replace_existing=True,
        )
        print("Добавлена задача 'monthly_mailing'.")

        try:
            print("Запуск планировщика...")
            scheduler.start()

        except KeyboardInterrupt:
            print("Остановка планировщика...")
            scheduler.shutdown()
            print("Планировщик успешно остановлен!")
