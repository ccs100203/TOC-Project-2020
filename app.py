import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", 'menu', 'walk', 'bike', 'roadside', 'street', 'handsome', 'noRespon', 'waitsign', 'rush'
            ,'direction', 'straight', 'left', 'road', 'pavement', 'sandwich', 'omelet', 'kaohsiung', 'tainan', 'remind', 'pickup', 'noRemind'],
    transitions=[
        {"trigger": "restart",   "source": ['walk', 'bike', 'roadside', 'street', 'handsome', 'noRespon', 'waitsign', 'rush'
            ,'direction', 'straight', 'left', 'road', 'pavement', 'sandwich', 'omelet', 'kaohsiung', 'tainan', 'remind', 'pickup', 'noRemind'],   "dest": "menu",},
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
        {"trigger": "advance",   "source": "road",   "dest": "omelet",   "conditions": "is_going_to_omelet",},
        {"trigger": "advance",   "source": "sandwich",   "dest": "kaohsiung",   "conditions": "is_going_to_kaohsiung",},
        {"trigger": "advance",   "source": "sandwich",   "dest": "tainan",   "conditions": "is_going_to_tainan",},
        {"trigger": "advance",   "source": "tainan",   "dest": "remind",   "conditions": "is_going_to_remind",},
        {"trigger": "advance",   "source": "tainan",   "dest": "pickup",   "conditions": "is_going_to_pickup",},
        {"trigger": "advance",   "source": "tainan",   "dest": "noRemind",   "conditions": "is_going_to_noRemind",},
        
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
        # if response == False:
            # send_text_message(event.source.user_id, f"no change in: {machine.state}")
        if response == False and machine.state == 'user':
            send_text_message(event.reply_token, TextSendMessage(text="輸入: \"start\""))
        

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
