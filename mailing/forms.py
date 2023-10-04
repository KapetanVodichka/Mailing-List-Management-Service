from django import forms
from .models import Mailing, Mail, Client


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        # fields = '__all__'
        exclude = ('mailing_status', )

        widgets = {
            'starting_at': forms.TimeInput(attrs={'type': 'time'}),
            'ending_at': forms.TimeInput(attrs={'type': 'time'}),
        }


class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = '__all__'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('mailing',)