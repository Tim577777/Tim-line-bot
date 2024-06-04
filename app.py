from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent

import sys

app = Flask(__name__)

configuration = Configuration(access_token='mjtPHSJ5iOAUDtnN8lQkNbsV0Yam1XPXu1ehiRxkru6jQpq7zBZo2CZZI8PmYgurTBkivchb5PZPdEgejnvAoQxMdQhf07lG3VdgPzV757T9ZQOxqDbPolc8XaY5lV5gSXBb/TKNK1aGyrdiHjfbuAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f65cd768c3d54ea3de80bd7699d2f725')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    #sys.stderr('f\n')

    # handle webhook body
    try:
        handler.handle(body, signature)
        print('f\n')
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info( ReplyMessageRequest( reply_token=event.reply_token, messages=[TextMessage(text=event.message.text)]))

if __name__ == "__main__":
    app.run()