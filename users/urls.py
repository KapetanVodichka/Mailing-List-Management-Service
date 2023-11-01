from django.urls import path
from .views import MailingListView, MailingDetailView, MailingCreateView, MailCreateView, \
    ClientCreateView, MailingTemplateView, HomeView

app_name = 'mailing'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_template/', MailingTemplateView.as_view(), name='mailing_template'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mail_create/', MailCreateView.as_view(), name='mail_create'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
]