import json
import requests
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from bot.settings import ACCESS_TOKEN, VERIFY_TOKEN

from .models import DiscountCode, Client


def reply(user_id, msg):
    data = {
        'messaging_type': 'RESPONSE',
        'recipient': {'id': user_id},
        'message': {'text': msg},
    }
    requests.post("https://graph.facebook.com/v2.6/me/messages", params={'access_token': ACCESS_TOKEN}, json=data)


class HandleMessageView(View):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get("hub.mode") == "subscribe" and request.GET.get("hub.challenge"):
            if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
                return HttpResponse(self.request.GET['hub.challenge'])
            else:
                return HttpResponseForbidden('Error, invalid token')

        return HttpResponse('Bot is watching you!')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        if incoming_message['object'] == 'page':
            for entry in incoming_message['entry']:
                for message in entry['messaging']:
                    # Check to make sure the received call is a message call
                    # This might be delivery, optin, postback for other events
                    if 'message' in message:
                        fb_id = message['sender']['id']
                        msg = message['message']['text']
                        client = Client.objects.select_related('discount_code').fb_id(fb_id)
                        if client:
                            response = 'Otrzymałeś już swój kod rabatowy: {}. Dziękujemy za udział w promocji!'\
                                .format(client[0].discount_code.code)
                        else:
                            code = DiscountCode.objects.active().first()
                            if code:
                                if '@' in msg:
                                    if Client.objects.email(msg).exists():
                                        response = 'E-mail {} został już wykorzystany, podaj inny.'
                                    else:
                                        try:
                                            client = Client(fb_id=fb_id, email=msg, discount_code=code)
                                            client.full_clean()
                                            client.save()
                                            code.is_active = False
                                            code.save()

                                            response = 'Gratuluję! Twój kod rabatowy to: {}'.format(code.code)

                                        except ValidationError as e:
                                            response = 'Wprowadź poprawny adres e-mail!'
                                else:
                                    response = 'Aby otrzymać kod rabatowy podaj swój e-mail!'
                            else:
                                response = 'Wszystkie kody rabatowe zostały wykorzystane, zapraszam później!'

                        reply(fb_id, response)

        return HttpResponse('OK')
