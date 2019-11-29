import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", 'menu', 'dead', 'walk', 'bike', 'roadside', 'street', 'handsome', 'noRespon', 'waitsign', 'rush'
            , 'straight', 'left', 'road', 'pavement', 'sandwich', 'FFF', 'radish', 'kaohsiung', 'tainan', 'remind', 'pickup', 'noRemind'],
    transitions=[
        {"trigger": "die",   "source": ['roadside', 'handsome', 'waitsign', 'rush', 'left', 'pavement', 'radish', 'kaohsiung', 'pickup'],   "dest": "dead",},
        {"trigger": "advance",   "source": "dead",   "dest": "menu",   "conditions": "dead_going_to_menu",},
        {"trigger": "advance",   "source": ['menu', 'dead', 'walk', 'bike', 'roadside', 'street', 'handsome', 'noRespon', 'waitsign', 'rush'
            , 'straight', 'left', 'road', 'pavement', 'sandwich', 'radish', 'kaohsiung', 'tainan', 'remind', 'pickup', 'noRemind'],   "dest": "user", "conditions": "is_going_to_user",},
        {"trigger": "happy",   "source": ['noRemind', 'remind'],   "dest": "user",},
        {"trigger": "advance",   "source": "user",   "dest": "menu",   "conditions": "is_going_to_menu",},
        {"trigger": "advance",   "source": "menu",   "dest": "walk",   "conditions": "is_going_to_walk",},
        {"trigger": "advance",   "source": "menu",   "dest": "bike",   "conditions": "is_going_to_bike",},
        {"trigger": "advance",   "source": ["walk",'straight'],   "dest": "roadside",   "conditions": "is_going_to_roadside",},
        {"trigger": "advance",   "source": "walk",   "dest": "street",   "conditions": "is_going_to_street",},
        {"trigger": "advance",   "source": "street",   "dest": "handsome",   "conditions": "is_going_to_handsome",},
        {"trigger": "advance",   "source": "street",   "dest": "noRespon",   "conditions": "is_going_to_noRespon",},
        {"trigger": "advance",   "source": "noRespon",   "dest": "waitsign",   "conditions": "is_going_to_waitsign",},
        {"trigger": "advance",   "source": "noRespon",   "dest": "rush",   "conditions": "is_going_to_rush",},
        {"trigger": "advance",   "source": "bike",   "dest": "straight",   "conditions": "is_going_to_straight",},
        {"trigger": "advance",   "source": "bike",   "dest": "left",   "conditions": "is_going_to_left",},
        {"trigger": "advance",   "source": "straight",   "dest": "road",   "conditions": "is_going_to_road",},
        {"trigger": "advance",   "source": "straight",   "dest": "pavement",   "conditions": "is_going_to_pavement",},
        {"trigger": "advance",   "source": "road",   "dest": "sandwich",   "conditions": "is_going_to_sandwich",},
        {"trigger": "advance",   "source": "road",   "dest": "radish",   "conditions": "is_going_to_radish",},
        {"trigger": "advance",   "source": "sandwich",   "dest": "kaohsiung",   "conditions": "is_going_to_kaohsiung",},
        {"trigger": "advance",   "source": "sandwich",   "dest": "tainan",   "conditions": "is_going_to_tainan",},
        {"trigger": "advance",   "source": "tainan",   "dest": "remind",   "conditions": "is_going_to_remind",},
        {"trigger": "advance",   "source": "tainan",   "dest": "pickup",   "conditions": "is_going_to_pickup",},
        {"trigger": "advance",   "source": "tainan",   "dest": "noRemind",   "conditions": "is_going_to_noRemind",},
        {"trigger": "advance",   "source": "sandwich",   "dest": "FFF",   "conditions": "is_going_to_FFF",},
        {"trigger": "burn_fff",   "source": "FFF",   "dest": "menu",},
        
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        # print(f"\nREQUEST BODY: \n{body}")
        # print(f'\nid: {event.source.user_id}')
        print(event.message.text)
        response = machine.advance(event)
        if response == False:
            if machine.state == 'user':
                button_message = TemplateSendMessage(
                    alt_text='Button',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://previews.123rf.com/images/abluecup/abluecup1410/abluecup141000071/32432764-a-red-button-with-the-word-warning-on-it.jpg',
                        title='開啟你的旅程',
                        text='Please select',
                        actions=[
                            MessageAction(
                                label='Start',
                                text='start'
                            ),
                            MessageAction(
                                label='No Start',
                                text='start'
                            ),
                        ]
                    )
                )
                send_text_message(event.reply_token, button_message)
            elif event.message.text.lower() == 'now':
                send_text_message(event.reply_token, TextSendMessage(text=f"State: {machine.state}"))
        
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
