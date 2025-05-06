from django.urls import path
from .views import WebhookView, ConversationListView, ConversationDetail

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook'),
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    path('conversations/<uuid:id>/', ConversationDetail.as_view(), name='conversation-detail'),
]
