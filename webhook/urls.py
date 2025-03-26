from django.urls import path
from .views import whatsapp_webhook, api_root

urlpatterns = [
    path("", api_root, name="api_root"),
    path("webhook/", whatsapp_webhook, name="whatsapp_webhook"),
    
]
