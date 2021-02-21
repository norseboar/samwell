import logging
import os

from flask import request
from slack_sdk import WebClient

from app import app
from .lib import decide_is_question

REQUEST_TYPE_EVENT = 'event_callback'
REQUEST_TYPE_VERIFICATION = 'url_verification'
EVENT_TYPE_MESSAGE = 'message'
BOT_USER_ID = os.environ['BOT_USER_ID']

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

@app.route('/')
def home():
    return "hello world"

@app.route('/slack-events', methods=['GET', 'POST'])
def slack_events():
    data = request.get_json()

    request_type = data['type']

    if request_type == REQUEST_TYPE_VERIFICATION:
        app.logger.info('Received challenge')
        return data['challenge']

    if request_type != REQUEST_TYPE_EVENT:
        app.logger.info(data)
        return {}
    
    event_type = data['event']['type']

    if event_type == EVENT_TYPE_MESSAGE:
        message_text = data['event']['text']

        if "debug" in message_text:
            app.logger.info(data)

        app.logger.info('Received message {}'.format(message_text))
        if decide_is_question(message_text) and data['event']['user'] != BOT_USER_ID:
            thread_ts = data['event'].get('thread_ts') or data['event']['ts']
            client.chat_postMessage(channel='#integration-test', text='Did somebody say question?', thread_ts=thread_ts)
        return {}
    else:
        app.logger.info(data)
        return {}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
