from django import forms
from django.forms import DateTimeInput

from .models import Mailing, Mail, Client


class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['mail_theme', 'mail_body']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'patronymic', 'email', 'comment']


class MailingForm(forms.ModelForm):
    mail_theme = forms.CharField(max_length=150, label='Тема', required=False)
    mail_body = forms.CharField(widget=forms.Textarea, label='Тело сообщения', required=False)

    class Meta:
        model = Mailing
        fields = ['period', 'starting_at', 'ending_at', 'clients']

        widgets = {
            'starting_at': DateTimeInput(attrs={'type': 'datetime-local'}),
            'ending_at': DateTimeInput(attrs={'type': 'datetime-local'}),
        }