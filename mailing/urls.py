from django.urls import path
from django.views.decorators.cache import cache_page

from .views import MailingListView, MailingDetailView, MailingCreateView, ClientCreateView, HomeView, \
    ClientListView, ClientUpdateView, ClientDeleteView, MailingDeleteView, MailingUpdateView, MailingOldListView

app_name = 'mailing'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('mailing_list/', cache_page(60)(MailingListView.as_view()), name='mailing_list'),
    path('mailing_list_old/', cache_page(60)(MailingOldListView.as_view()), name='mailing_list_old'),
    path('mailing_detail/<int:pk>/', cache_page(60)(MailingDetailView.as_view()), name='mailing_detail'),
    path('mailing_edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_list/', cache_page(60)(ClientListView.as_view()), name='client_list'),
    path('client_eidt/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]
