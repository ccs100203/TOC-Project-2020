import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, text)
    return "OK"



# def send_image_url(reply_token, img_url):
    # line_bot_api = LineBotApi(channel_access_token)
    # line_bot_api.reply_message(reply_token, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    # line_bot_api.push_message(reply_token, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    # return 'OK'


# def send_button_message(reply_token, text):
    # line_bot_api = LineBotApi(channel_access_token)
    # buttons_template_message = TemplateSendMessage(
    #     alt_text='Buttons',
    #     template=ButtonsTemplate(
    #         thumbnail_image_url='https://i.imgur.com/0bRwX17.jpg',
    #         title='Menu',
    #         text='Please select',
    #         actions=[
    #             MessageAction(
    #                 label='message',
    #                 text='message text'
    #             ),
    #             MessageAction(
    #                 label='start',
    #                 text='start'
    #             ),
    #         ]
    #     )
    # )
    # line_bot_api.reply_message(reply_token, buttons_template_message)
    # return 'OK'
