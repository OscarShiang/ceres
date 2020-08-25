#! python

from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, StickerMessage
)

app = Flask(__name__)

# channel access token
linebot_api = LineBotApi('')

# channel secret
handler = WebhookHandler('')

# listen post request from '/callback'
@app.route('/callback', methods = ['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text = True)
    app.logger.info('Request body: ' + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    linebot_api.reply_message(event.reply_token, TextSendMessage(text = event.message.text))

import os
if __name__ == '__main__':
    port = int(os.environ.get('POST', 5000))
    app.run(host = '0.0.0.0', port = port)