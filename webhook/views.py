import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
import logging

import requests
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

    
            api_url = f"https://graph.facebook.com/v15.0/644753268711147/messages"

            phone_number = data.get("phone_number", "").replace("p:", "").strip()
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "template",
                "template": {"name": "hello_world", "language": {"code": "en_US"}},
            }


            headers={
                    "Authorization": "Bearer EAAQ2FI7LFkYBO7ycAAmlNilxvBrl77WkWwM54cOisCxThZBOwyQizOQstHoQhI8VASUlvH05aDZAwqVQLEA6kqt6r2m5GAZCeZC538IibHX0gJOd50ISEOplwyPPbLTHm7YpYIGALMHAAZCqrG6YVLsUmSWbvOqZC8gnQPY2OpZBeOTJRFsc1uQesWlx37IyLsBdJGFOaXLO6f1EU7BPBO8VhwLuyZACtqnVjZCfRWxsU",
                    "Content-Type": "application/json",
                }
        
            payload = json.dumps(payload)

            response = requests.request("POST", api_url, headers=headers, data=payload)
            logger.info(f"message  response {response}")
            return JsonResponse({"status": "success", "message": "Data received"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
