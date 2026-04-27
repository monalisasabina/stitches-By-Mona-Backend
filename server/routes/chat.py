from flask_restful import Resource
from flask import request
from chatbot.chatbot_responses import RESPONSES, DEFAULT_RESPONSE


class Chat(Resource):
    def post(self):
        data = request.get_json()

        message = data.get('message', '').lower().strip()

        if not message:
            return {'error': 'message is required'}, 400

        # check for keyword matches
        response = None
        for keyword, reply in RESPONSES.items():
            if keyword in message:
                response = reply
                break

        if not response:
            response = DEFAULT_RESPONSE

        return {'response': response}, 200