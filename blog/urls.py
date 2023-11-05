from django.urls import path
from django.views.decorators.cache import cache_page

from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = 'blog'

urlpatterns = [
    path('', cache_page(60)(BlogListView.as_view()), name='list'),
    path('create/', BlogCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
    path('view/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='view'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
]
