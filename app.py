from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('RU3EUFpE8F8KxQ9YczQN8XSKM6gquB9T5ujG9N2jTeZczea6UvoVzB7roD6+rib0aJ6SNhxEST4zFQL1crO7b8EbwfoDCrpCG1KI/sirwKKEod7TBZ2Hut2firBY8k1X25njfQzQfC7CnmkRuTaTxQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('97e1f7c1d7e3e49cabfca35be86d5735')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()