from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.models import Blog


class BlogListView(ListView):
    model = Blog


class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Blog
    fields = ('title', 'body', 'preview',)

    def get_success_url(self):
        return reverse('blog:view', args=[self.object.pk])

    def test_func(self):
        return self.request.user.is_manager


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ('title', 'body', 'preview',)
    permission_required = 'blog.edit_blog'

    def get_success_url(self):
        return reverse('blog:view', args=[self.object.pk])

    def test_func(self):
        return self.request.user.is_manager


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    permission_required = 'blog.delete_blog'
    success_url = reverse_lazy('blog:list')

    def test_func(self):
        return self.request.user.is_manager