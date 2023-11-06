from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
import random

from users.forms import UserRegisterForm
from users.models import User

lower = 'abcdefghijklmnopqrstuvwxyz'
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'

symbols = lower + upper + numbers
length = 20


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        super().form_valid(form)
        code = ''.join(random.sample(symbols, length))
        self.object.code = code
        self.object.save()

        url_ = self.request.build_absolute_uri(reverse('users:verify_email', kwargs={
            'code': code
        }))

        send_mail(
            'Подтверждение регистрации',
            f'Подтвердите регистрацию перейдя по ссылке: {url_}',
            'catalog.course@mail.ru',
            [self.object.email]
        )

        return HttpResponseRedirect(self.get_success_url())


class VerifyEmailView(View):
    template_name = 'users/verify_email.html'
    success_url = reverse_lazy('users:login')

    def get(self, request, code):
        user = get_object_or_404(User, code=code)
        user.is_active = True
        user.save()
        return redirect('users:login')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile_edit.html'
    fields = ['first_name', 'last_name', 'email', 'country', 'phone']

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:profile')


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/profile_confirm_delete.html'
    success_url = reverse_lazy('mailing:home')

    def get_object(self, queryset=None):
        return self.request.user
