from django import forms
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
    # Поля для темы сообщения и его тела
    mail_theme = forms.CharField(max_length=150, label='Тема', required=False)
    mail_body = forms.CharField(widget=forms.Textarea, label='Тело сообщения', required=False)

    class Meta:
        model = Mailing
        fields = ['period', 'starting_at', 'ending_at', 'clients']  # Добавляем поле 'mail'

        widgets = {
            'starting_at': forms.TimeInput(attrs={'type': 'time'}),
            'ending_at': forms.TimeInput(attrs={'type': 'time'}),
        }