import json
import requests

from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import View

from bot.settings import ACCESS_TOKEN, VERIFY_TOKEN


def reply(user_id, msg):
    data = {
        'recipient': {'id': user_id},
        'message': {'text': msg},
    }
    requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)


class HandleMessageView(View):
    def get(self, request, *args, **kwargs):
        if self.request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
                return HttpResponse(self.request.GET['hub.challenge'])
            else:
                return HttpResponseForbidden('Error, invalid token')

        return HttpResponse('Bot is watching you!')

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    reply(message['sender']['id'], message['message']['text'])

        return HttpResponse()