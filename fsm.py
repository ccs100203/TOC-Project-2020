from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_url
from linebot.models import MessageEvent, TextMessage, TextSendMessage

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def on_enter_user(self, event):
        print("I'm entering user")

    def on_exit_user(self, event):
        print("Leaving user")
        send_text_message(event.reply_token, [TextSendMessage(text="早上起床，發現快遲到了\n選擇你的交通方式"), TextSendMessage(text="輸入:\"走路\" \"機車\" \"腳踏車\"")])

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "start"

    # def on_enter_menu(self, event):

    #menu to walk
    def is_going_to_walk(self, event):
        text = event.message.text
        return text.lower() == "走路"

    def on_enter_walk(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="健康的走路\n該走哪條呢?"), TextSendMessage(text="輸入:\"路緣\" \"騎樓\" \"人行道\"")])
        
    #menu to bike
    def is_going_to_bike(self, event):
        text = event.message.text
        return text.lower() == "腳踏車" or text.lower() == "機車"

    def on_enter_bike(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="你在系館東北邊，你面向南邊\n該往哪騎?"), TextSendMessage(text="輸入:\"直走\" \"左轉\" \"右轉\"")])
    
    #walk/straight to roadside
    def is_going_to_roadside(self, event):
        text = event.message.text
        return text.lower() == "路緣"

    def on_enter_roadside(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="突然有卡車切進去\n在台南還敢走路緣啊\n人生登出"), TextSendMessage(text="選錯了\n重新開始吧"), TextSendMessage(text="早上起床，發現快遲到了\n選擇你的交通方式"), TextSendMessage(text="輸入:\"走路\" \"機車\" \"腳踏車\"")] )
        self.restart(event)

    #walk to street
    def is_going_to_street(self, event):
        text = event.message.text
        return text.lower() == "騎樓" or text.lower() == "人行道"

    def on_enter_street(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="此時路過市集\n突然有女生大喊「帥哥」~~"), TextSendMessage(text="輸入:\"帥爆 回頭\" \"不理他\"")])

    #street to handsome
    def is_going_to_handsome(self, event):
        text = event.message.text
        return text.lower() == "帥爆 回頭" or text.lower() == "帥爆" or text.lower() == "回頭"

    def on_enter_handsome(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="結果只是個大媽叫你\n結果被她纏上導致遲到\n近女色 失敗"), TextSendMessage(text="選錯了\n重新開始吧"), TextSendMessage(text="早上起床，發現快遲到了\n選擇你的交通方式"), TextSendMessage(text="輸入:\"走路\" \"機車\" \"腳踏車\"")] )
        self.restart(event)

    #street to noRespon
    def is_going_to_noRespon(self, event):
        text = event.message.text
        return text.lower() == "不理他" or text.lower() == "不理她"

    def on_enter_noRespon(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="到了馬路口，遇到紅燈\n看起來四周無車"), TextSendMessage(text="輸入:\"等紅燈\" \"衝過去\" ")])

    #noRespon to waitsign
    def is_going_to_waitsign(self, event):
        text = event.message.text
        return text.lower() == "等紅燈"

    def on_enter_waitsign(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="乖乖等紅燈，安全到達系館\n但已經遲到了\n小孩子才走路"), TextSendMessage(text="選錯了\n重新開始吧"), TextSendMessage(text="早上起床，發現快遲到了\n選擇你的交通方式"), TextSendMessage(text="輸入:\"走路\" \"機車\" \"腳踏車\"")] )
        self.restart(event)

    #noRespon to rush
    def is_going_to_rush(self, event):
        text = event.message.text
        return text.lower() == "衝過去"

    def on_enter_rush(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="加速跑過去，結果就撞車了\n在台南還敢闖紅燈啊"), TextSendMessage(text="選錯了\n重新開始吧"), TextSendMessage(text="早上起床，發現快遲到了\n選擇你的交通方式"), TextSendMessage(text="輸入:\"走路\" \"機車\" \"腳踏車\"")] )
        self.restart(event)
    

    #bike to straight
    def is_going_to_straight(self, event):
        text = event.message.text
        return text.lower() == "直走" or text.lower() == "右轉"

    def on_enter_straight(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="騎對了方向\n再選條路吧~"), TextSendMessage(text="輸入:\"馬路\" \"騎樓\" \"路緣\" ")])

    #bike to left
    def is_going_to_left(self, event):
        text = event.message.text
        return text.lower() == "左轉"

    def on_enter_left(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="迷路啦\n乖乖遲到吧"), TextSendMessage(text="選錯了\n重新開始吧"), TextSendMessage(text="早上起床，發現快遲到了\n選擇你的交通方式"), TextSendMessage(text="輸入:\"走路\" \"機車\" \"腳踏車\"")] )
        self.restart(event)

    #straight to road
    def is_going_to_road(self, event):
        text = event.message.text
        return text.lower() == "馬路"

    def on_enter_road(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="騎一騎肚子餓了，騎到早餐店\n買什麼早餐?"), TextSendMessage(text="輸入:\"現成的三明治\" \"現煎的蘿蔔糕\" \"現煎的蛋餅\" ")])
    
    #straight to pavement
    def is_going_to_pavement(self, event):
        text = event.message.text
        return text.lower() == "騎樓"

    def on_enter_pavement(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="台南的騎樓怎麼可能是空的呢\n早就推滿東西啦"), TextSendMessage(text="選錯了\n重新開始吧"), TextSendMessage(text="早上起床，發現快遲到了\n選擇你的交通方式"), TextSendMessage(text="輸入:\"走路\" \"機車\" \"腳踏車\"")] )
        self.restart(event)

    #road to sandwich
    def is_going_to_sandwich(self, event):
        text = event.message.text
        return text.lower() == "現成的三明治" or text.lower() == "三明治"

    def on_enter_sandwich(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="買完離開早餐店\n終於快到系館了\n遭遇了紅燈"), TextSendMessage(text="輸入:\"等紅燈\" \"台南式右轉\" \"高雄式左轉\" ")])
    
    #road to omelet
    def is_going_to_omelet(self, event):
        text = event.message.text
        return text.lower() == "現煎的蘿蔔糕" or text.lower() == "蘿蔔糕" or text.lower() == "現煎的蛋餅" or text.lower() == "蛋餅"

    def on_enter_omelet(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="早餐店煎太久了\n遲到啦啦啦"), TextSendMessage(text="選錯了\n重新開始吧"), TextSendMessage(text="早上起床，發現快遲到了\n選擇你的交通方式"), TextSendMessage(text="輸入:\"走路\" \"機車\" \"腳踏車\"")] )
        self.restart(event)

    #sandwich to kaohsiung
    def is_going_to_kaohsiung(self, event):
        text = event.message.text
        return text.lower() == "高雄式左轉" or text.lower() == "高雄" or text.lower() == "左轉"

    def on_enter_kaohsiung(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="這裡可是台南欸!\n直接撞上另一台橫向跨越馬路的車"), TextSendMessage(text="選錯了\n重新開始吧"), TextSendMessage(text="早上起床，發現快遲到了\n選擇你的交通方式"), TextSendMessage(text="輸入:\"走路\" \"機車\" \"腳踏車\"")] )
        self.restart(event)
    
    #sandwich to tainan
    def is_going_to_tainan(self, event):
        text = event.message.text
        return text.lower() == "台南式右轉" or text.lower() == "台南" or text.lower() == "右轉" or text.lower() == "等紅燈"

    def on_enter_tainan(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="到了地停前\n發現旁邊的正妹皮包掉了，你應該?"), TextSendMessage(text="輸入:\"提醒他\" \"撿走\" \"不理她\" ")])

    #tainan to remind
    def is_going_to_remind(self, event):
        text = event.message.text
        return text.lower() == "提醒他" or text.lower() == "提醒她"

    def on_enter_remind(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="Happy End\n雖然遲到了，但得到了正妹的line"), TextSendMessage(text="恭喜通關~\n輸入\"start\"可再來一次")])
        self.happy(event)

    #tainan to pickup
    def is_going_to_pickup(self, event):
        text = event.message.text
        return text.lower() == "撿" or text.lower() == "撿走"

    def on_enter_pickup(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="私藏時被抓包\n警察局見"), TextSendMessage(text="選錯了\n重新開始吧"), TextSendMessage(text="早上起床，發現快遲到了\n選擇你的交通方式"), TextSendMessage(text="輸入:\"走路\" \"機車\" \"腳踏車\"")] )
        self.restart(event)

    #tainan to noRemind
    def is_going_to_noRemind(self, event):
        text = event.message.text
        return text.lower() == "不理他" or text.lower() == "不理她"

    def on_enter_noRemind(self, event):
        send_text_message(event.reply_token, [TextSendMessage(text="True End\n準時抵達教室，上課囉~"), TextSendMessage(text="恭喜通關~\n輸入\"start\"可再來一次")])
        self.happy(event)