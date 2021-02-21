import logging

from app import app

from flask import request

@app.route('/')
def home():
    return "hello world"

@app.route('/slack-events', methods=['GET', 'POST'])
def slack_events():
    data = request.get_json()

    request_type = data['type']

    if request_type == 'url_verification':
        app.logger.info('Received challenge')
        return data['challenge']
    else:
        app.logger.info(data['event']['text'])
        return {}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
