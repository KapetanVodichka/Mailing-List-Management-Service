import logging
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from config.settings import EMAIL_USE_SSL, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from mailing.models import Mailing, Log

logger = logging.getLogger(__name__)


def my_job():
    # Получаем текущее время
    current_time = datetime.now().strftime("%H:%M")

    print(f"Задача 'my_job' запущена в {current_time}")

    # Получаем активные рассылки, которые должны быть отправлены в данный момент
    active_mailings = Mailing.objects.filter(starting_at=current_time,
                                             mailing_status='Создана')

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
                server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
                if EMAIL_USE_SSL:
                    server.starttls()
                server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

                msg = MIMEMultipart()
                msg['From'] = EMAIL_HOST_USER
                msg['To'] = client.email
                msg['Subject'] = mail_theme

                msg.attach(MIMEText(mail_body, 'plain'))

                server.sendmail(EMAIL_HOST_USER, client.email, msg.as_string())
                server.quit()
                print('вроде как отправили письмо')

                # Обновляем лог рассылки
                log = Log(mailing=mailing, last_try_time=datetime.now(), status='Отправлено',
                          mail_server_callback='Успешно отправлено')
                log.save()

            except Exception as e:
                # Обработка ошибок
                log = Log(mailing=mailing, last_try_time=datetime.now(), status='Ошибка', mail_server_callback=str(e))
                log.save()
                print(f'ошибка {e}')

        # Обновляем статус рассылки на "Завершена"
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
            my_job,
            trigger=CronTrigger(second="*/10"),  # Запускать каждые 10 секунд
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        print("Добавлена задача 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю в полночь в понедельник
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        print("Добавлена еженедельная задача: 'delete_old_job_executions'.")

        try:
            print("Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            print("Остановка планировщика...")
            scheduler.shutdown()
            print("Планировщик успешно остановлен!")
