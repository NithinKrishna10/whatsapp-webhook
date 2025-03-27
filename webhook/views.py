import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
import logging
# Set up logging
logger = logging.getLogger(__name__)

VERIFY_TOKEN = "your_verify_token"

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse("Invalid verification token", status=403)

    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        print("Received WhatsApp Message:", json.dumps(data, indent=2))
        return HttpResponse("received", status=200)

    return HttpResponse("Invalid request", status=400)


def api_root(request):
    data = {
        'message': 'Welcome to the WhatsApp Webhook API',
        'endpoints': [
            {
                'url': 'webhook/',
                'description': 'WhatsApp incoming message webhook',
            },
        ],
    }
    return JsonResponse(data)


@csrf_exempt  # Allows webhook to send POST requests without CSRF token
def google_sheets_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON payload
            

            logger.info(f"Received updated value: {data}")

            return JsonResponse({"status": "success", "message": "Data received"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
