from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.models import Blog
from blog.permissions import ManagerMixin


class BlogListView(ListView):
    model = Blog


class BlogCreateView(LoginRequiredMixin, ManagerMixin, CreateView):
    model = Blog
    fields = ('title', 'body', 'preview',)

    def get_success_url(self):
        return reverse('blog:view', args=[self.object.pk])


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, ManagerMixin, UpdateView):
    model = Blog
    fields = ('title', 'body', 'preview',)

    def get_success_url(self):
        return reverse('blog:view', args=[self.object.pk])


class BlogDeleteView(LoginRequiredMixin, ManagerMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
