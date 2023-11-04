from django.contrib import admin

from mailing.models import Client, Mailing, Mail, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patronymic', 'email', 'comment')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('period', 'starting_at', 'ending_at', 'mailing_status')


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('mail_theme', 'mail_body')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('last_mailing_datetime', 'status', 'mail_server_callback', 'mailing')