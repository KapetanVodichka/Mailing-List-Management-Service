from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, FormView
from django.urls import reverse_lazy, reverse

from blog.models import Blog
from .forms import MailingForm, MailForm, ClientForm
from .models import Client, Mailing, Mail, Log


class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Количество рассылок всего
        total_mailings = Mailing.objects.count()

        # Количество активных рассылок (не завершенных)
        active_mailings = Mailing.objects.exclude(mailing_status='Завершена').count()

        # Количество уникальных клиентов для рассылок
        unique_clients = Client.objects.count()

        # 3 случайные статьи из блога
        random_articles = Blog.objects.order_by('?')[:3]

        context['total_mailings'] = total_mailings
        context['active_mailings'] = active_mailings
        context['unique_clients'] = unique_clients
        context['random_articles'] = random_articles

        return context


class MailingTemplateView(FormView):
    template_name = 'mailing/mailing_template.html'
    form_class = MailingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_form'] = MailingForm()
        context['mail_form'] = MailForm()
        context['client_form'] = ClientForm()
        return context

    @transaction.atomic
    def form_valid(self, form):
        # Создаем сообщение
        mail = Mail.objects.create(
            mail_theme=form.cleaned_data['mail_theme'],
            mail_body=form.cleaned_data['mail_body']
            # Дополните это соответствующими полями вашей формы
        )

        # Создаем рассылку и связываем с сообщением
        mailing = Mailing.objects.create(mail=mail)
        # Дополнительная логика для сохранения данных рассылки

        return redirect('mailing:mailing_list')

    def form_invalid(self, form):
        # Обработка ошибок валидации формы
        return self.render_to_response(self.get_context_data(form=form))


# Представление для списка рассылок
class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'


# Представление для создания новой рассылки
class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'

    def get_success_url(self):
        return reverse('mailing:mailing_list')

    def form_valid(self, form):
        # Создаем сообщение при сохранении рассылки
        mail = Mail(
            mail_theme=form.cleaned_data['mail_theme'],
            mail_body=form.cleaned_data['mail_body']
        )
        mail.save()

        # Сохраняем рассылку и связываем её с созданным сообщением
        mailing = form.save(commit=False)
        mailing.mail = mail
        mailing.save()

        return super().form_valid(form)


class MailCreateView(CreateView):
    model = Mail
    form_class = MailForm
    template_name = 'mailing/mail_form.html'

    def get_success_url(self):
        # При успешном создании сообщения, перенаправляем на страницу создания клиента
        return reverse('mailing:client_create', kwargs={'pk': self.object.id})


# Представление для создания клиента
class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:mailing_list')
    template_name = 'mailing/client_form.html'


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


