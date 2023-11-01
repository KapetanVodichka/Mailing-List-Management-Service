# from apscheduler.schedulers.background import BackgroundScheduler
# from django.conf import settings
# from django_apscheduler.jobstores import DjangoJobStore
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime
# from .models import Mailing, Log
#
# EMAIL_BACKEND = settings.EMAIL_BACKEND
# EMAIL_HOST = settings.EMAIL_HOST
# EMAIL_PORT = settings.EMAIL_PORT
# EMAIL_USE_SSL = settings.EMAIL_USE_SSL
# EMAIL_HOST_USER = settings.EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
#
# scheduler = BackgroundScheduler(jobstores={"default": DjangoJobStore()})
#
#
# def send_mailings():
#     # Получаем текущее время
#     current_time = datetime.now().strftime("%H:%M")
#
#     # Получаем активные рассылки, которые должны быть отправлены в данный момент
#     active_mailings = Mailing.objects.filter(starting_at__lte=current_time, ending_at__gte=current_time,
#                                              mailing_status='Создана')
#
#     for mailing in active_mailings:
#         # Обновляем статус рассылки на "Запущена"
#         mailing.mailing_status = 'Запущена'
#         mailing.save()
#
#         # Получаем клиентов, которые должны получить это сообщение
#         clients = mailing.clients.all()
#
#         for client in clients:
#             # Извлекаем theme и body из объекта Mail
#             mail_theme = mailing.mail.mail_theme
#             mail_body = mailing.mail.mail_body
#
#             try:
#                 # Отправляем письмо
#                 server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
#                 if EMAIL_USE_SSL:
#                     server.starttls()
#                 server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#
#                 msg = MIMEMultipart()
#                 msg['From'] = EMAIL_HOST_USER
#                 msg['To'] = client.email
#                 msg['Subject'] = mail_theme
#
#                 msg.attach(MIMEText(mail_body, 'plain'))
#
#                 server.sendmail(EMAIL_HOST_USER, client.email, msg.as_string())
#                 server.quit()
#
#                 # Обновляем лог рассылки
#                 log = Log(mailing=mailing, last_try_time=datetime.now(), status='Отправлено',
#                           mail_server_callback='Успешно отправлено')
#                 log.save()
#
#             except Exception as e:
#                 # Обработка ошибок
#                 log = Log(mailing=mailing, last_try_time=datetime.now(), status='Ошибка', mail_server_callback=str(e))
#                 log.save()
#
#         # Обновляем статус рассылки на "Завершена"
#         mailing.mailing_status = 'Завершена'
#         mailing.save()
#
#
# scheduler.add_job(send_mailings, "interval", seconds=15, start_date="2023-01-01 00:00:00")
#
# scheduler.start()