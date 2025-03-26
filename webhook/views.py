import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

VERIFY_TOKEN = "your_verify_token"

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge
        else:
            return JsonResponse({"error": "Invalid verification token"}, status=403)

    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        print("Received WhatsApp Message:", json.dumps(data, indent=2))
        return JsonResponse({"status": "received"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)



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
