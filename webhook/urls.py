from django.urls import path
from .views import whatsapp_webhook, api_root, google_sheets_webhook

urlpatterns = [
    path("", api_root, name="api_root"),
    path("webhook/", whatsapp_webhook, name="whatsapp_webhook"),
    path("google-sheet/", google_sheets_webhook, name="google-sheet-webhook"),
]
