from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
import random

from users.forms import UserRegisterForm
from users.models import User

User = get_user_model()

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
        form_users = super().form_valid(form)
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
        user = User.objects.get(code=code)
        user.is_active = True
        user.save()
        return redirect('users:login')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        # Возвращает объект пользователя, который будет отображаться в профиле
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


# class UpdatePassView(View):
#     template_name = 'users/update_pass.html'
#
#     def get(self, request):
#         return render(request, self.template_name)
#
#     def post(self, request):
#         email = request.POST.get('email')
#         try:
#             user = User.objects.get(email=email)
#             new_pass = ''.join(random.sample(symbols, length))
#             user.set_password(new_pass)
#             user.save()
#
#             send_mail(
#                 'Ваш новый пароль',
#                 f'Пароль забыли, хоть с нового кайфуйте: {new_pass}',
#                 'catalog.course@mail.ru',
#                 [user.email]
#             )
#
#             return HttpResponseRedirect(reverse('users:login'))
#         except User.DoesNotExist:
#             return render(request, self.template_name, {'error': 'Пользователь с таким email не найден.'})


# def updatepassword(request):
#     if request.user.is_authenticated:
#         new_pass = ''.join(random.sample(symbols, length))
#         request.user.set_password(new_pass)
#         request.user.save()
#
#         send_mail(
#             'Ваш новый пароль',
#             f'Ваш новый пароль: {new_pass}',
#             'catalog.course@mail.ru',
#             [request.user.email]
#         )
#         return redirect(reverse_lazy('users:update_pass'))
#     else:
#         return redirect('users:login')