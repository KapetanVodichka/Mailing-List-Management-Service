from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy

from .forms import MailingForm, MailForm, ClientForm
from .models import Client, Mailing, Mail, Log


class MailingTemplateView(TemplateView):
    template_name = 'mailing/mailing_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_form'] = MailingForm()
        context['mail_form'] = MailForm()
        context['client_form'] = ClientForm()
        return context


# Представление для списка рассылок
class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'


# Представление для создания новой рассылки
class MailingCreateView(CreateView):
    model = Mailing
    fields = ['period', 'mailing_time', 'mailing_status']
    template_name = 'mailing/mailing_form.html'


# Представление для обновления рассылки
class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['period', 'mailing_time', 'mailing_status']
    template_name = 'mailing/mailing_form.html'


# Представление для удаления рассылки
class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list.html')


# Представление для деталей рассылки
class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'


# Представление для списка клиентов
class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'


# Представление для деталей клиента
class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'


# Представление для создания клиента
class ClientCreateView(CreateView):
    model = Client
    fields = ['first_name', 'last_name', 'patronymic', 'email', 'comment']
    success_url = reverse_lazy('mailing: client_list')
    template_name = 'mailing/client_form.html'


# Представление для редактирования клиента
class ClientUpdateView(UpdateView):
    model = Client
    fields = ['first_name', 'last_name', 'patronymic', 'email', 'comment']
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('client_list')


# Представление для удаления клиента
class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client_list')
    template_name = 'mailing/client_confirm_delete.html'


