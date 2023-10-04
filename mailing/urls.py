from django.urls import path
from .views import MailingListView, MailingDetailView, MailingTemplateView

app_name = 'mailing'

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_template/', MailingTemplateView.as_view(), name='mailing_template'),
]