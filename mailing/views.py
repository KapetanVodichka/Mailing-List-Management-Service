from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from django_apscheduler.jobstores import DjangoJobStore

from blog.models import Blog
from blog.permissions import UserMixin
from config.settings import TIME_ZONE, CACHE_ENABLED
from .forms import MailingForm, ClientForm
from .models import Client, Mailing, Mail

scheduler = BackgroundScheduler(timezone=TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start()


class HomeView(TemplateView):
    """
        Главная страница
        """
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


class MailingListView(LoginRequiredMixin, UserMixin, ListView):
    """
    Представление для списка рассылок
    """
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        user = self.request.user
        # return Mailing.objects.filter(user=user)

        if CACHE_ENABLED:
            key = f'mailing_list_{user.id}'
            mailing_list = cache.get(key)
            if mailing_list is None:
                mailing_list = Mailing.objects.filter(user=user)
                cache.set(key, mailing_list)
        else:
            mailing_list = Mailing.objects.filter(user=user)
        return mailing_list


class MailingOldListView(LoginRequiredMixin, UserMixin, ListView):
    """
        Представление для списка архивных рассылок
        """
    model = Mailing
    template_name = 'mailing/mailing_list_old.html'

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(mailing_status='Завершена', user=user)


# Представление для создания новой рассылки
class MailingCreateView(LoginRequiredMixin, UserMixin, CreateView):
    """
        Представление для создания рассылки
        """
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
        mailing.user = self.request.user

        mailing.save()

        return super().form_valid(form)

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
        Представление для создания клиента
        """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:mailing_list')
    template_name = 'mailing/client_form.html'

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)


class MailingUpdateView(LoginRequiredMixin, UserMixin, UpdateView):
    """
        Представление для изменения существующей рассылки
        """
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)

    def get_success_url(self):
        return reverse('mailing:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        mailing = self.object
        if mailing.mail:
            form.fields['mail_theme'].initial = mailing.mail.mail_theme
            form.fields['mail_body'].initial = mailing.mail.mail_body
        form.fields['starting_at'].initial = mailing.starting_at
        form.fields['ending_at'].initial = mailing.ending_at
        return form


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """
        Представление для удаления рассылки
        """
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    """
        Представление для деталей рассылки
        """
    model = Mailing
    template_name = 'mailing/mailing_detail.html'

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)


class ClientListView(LoginRequiredMixin, ListView):
    """
    Представление для списка клиентов
    """
    model = Client
    template_name = 'mailing/client_list.html'

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для деталей клиента
    """
    model = Client
    template_name = 'mailing/client_detail.html'

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования клиента
    """
    model = Client
    fields = ['first_name', 'last_name', 'patronymic', 'email', 'comment']
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('users:client_list')

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления клиента
    """
    model = Client
    success_url = reverse_lazy('users:client_list')
    template_name = 'mailing/client_confirm_delete.html'

    def get_queryset(self):
        user = self.request.user
        return Mailing.objects.filter(user=user)


