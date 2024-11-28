from flask import Flask, request, abort
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from api.chatgpt import ChatGPT
import os



configuration = Configuration(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'
    
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )


# line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
# line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
# working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

# app = Flask(__name__)
# chatgpt = ChatGPT()

# @app.route('/')
# def home():
#     return 'Hello, World!'

# @app.route("/webhook", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#     # handle webhook body
#     try:
#         line_handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     except Exception as e:
#         app.logger.error(f"An error occurred: {e}")
#         abort(500)
#     return 'OK'

# @line_handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     global working_status
#     if event.message.type != "text":
#         return 'OK'


#     if event.message.text == "說話":
#         working_status = True
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text="我可以說話囉，歡迎來跟我互動 ^_^ "))
#         return 'OK'


#     if event.message.text == "閉嘴":
#         working_status = False
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text="好的，我乖乖閉嘴 > <，如果想要我繼續說話，請跟我說 「說話」 > <"))
#         return 'OK'


#     if working_status:
#         chatgpt.add_msg(f"HUMAN:{event.message.text}?\n")
#         reply_msg = chatgpt.get_response().replace("AI:", "", 1)
#         chatgpt.add_msg(f"AI:{reply_msg}\n")
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=reply_msg))


# if __name__ == "__main__":
#     app.run()
