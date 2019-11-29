from transitions.extensions import GraphMachine

from utils import send_text_message
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction


button_wakeup = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.elegantthemes.com/blog/wp-content/uploads/2018/11/how-to-wake-up-early.png',
                title='早上起床，發現快遲到了',
                text='選擇你的交通方式',
                actions=[
                    MessageAction(
                        label='走路',
                        text='走路'
                    ),
                    MessageAction(
                        label='機車',
                        text='機車'
                    ),
                    MessageAction(
                        label='腳踏車',
                        text='腳踏車'
                    ),
                ]
            )
        )

def get_button_die(url='https://pic.pimg.tw/keita240/1180170847.jpg', title='選錯了，重新開始吧', text='選錯了，重新開始吧'):
    return TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url=url,
                title=title,
                text=text,
                actions=[
                    MessageAction(
                        label='give up',
                        text='back'
                    ),
                    MessageAction(
                        label='restart',
                        text='restart'
                    ),
                ]
            )
        )

class TocMachine(GraphMachine):
    global button_wakeup
    
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    #all to user
    def is_going_to_user(self, event):
        text = event.message.text
        isBack = text.lower() == "back"
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
        if isBack:
            send_text_message(event.reply_token, button_message)
        return isBack

    # def on_enter_user(self, event):
    #     print("I'm entering user")

    def on_exit_user(self, event):
        print("Leaving user")
        send_text_message(event.reply_token, button_wakeup)

    def dead_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "restart"

    def on_exit_dead(self, event):
        print("Leaving dead")
        if event.message.text == "restart":
            send_text_message(event.reply_token, button_wakeup)

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "start"

    # def on_enter_menu(self, event):

    #menu to walk
    def is_going_to_walk(self, event):
        text = event.message.text
        return text.lower() == "走路"

    def on_enter_walk(self, event):
        button_message = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.insurancejournal.com/app/uploads/2018/06/crossroad-580x466.jpg',
                title='健康的走路，該走哪條呢?',
                text='Please select',
                actions=[
                    MessageAction(
                        label='路緣',
                        text='路緣'
                    ),
                    MessageAction(
                        label='騎樓',
                        text='騎樓'
                    ),
                    MessageAction(
                        label='人行道',
                        text='人行道'
                    ),
                ]
            )
        )
        send_text_message(event.reply_token, button_message)
        
    #menu to bike
    def is_going_to_bike(self, event):
        text = event.message.text
        return text.lower() == "腳踏車" or text.lower() == "機車"

    def on_enter_bike(self, event):
        button_message = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://media.istockphoto.com/vectors/arrow-cross-three-way-thin-line-icon-linear-vector-symbol-vector-id843181676',
                title='你在系館東北邊，你面向南邊，該往哪騎?',
                text='Please select',
                actions=[
                    MessageAction(
                        label='直走',
                        text='直走'
                    ),
                    MessageAction(
                        label='左邊',
                        text='左邊'
                    ),
                    MessageAction(
                        label='右邊',
                        text='右邊'
                    ),
                ]
            )
        )
        send_text_message(event.reply_token, button_message)
    
    #walk/straight to roadside
    def is_going_to_roadside(self, event):
        text = event.message.text
        return text.lower() == "路緣"

    def on_enter_roadside(self, event):
        img_url = 'https://comps.canstockphoto.com.tw/%E5%8D%A1%E8%BB%8A-%E5%8D%A1%E9%80%9A-%E5%9C%96%E8%B1%A1-%E7%85%A7%E7%89%87_csp47765617.jpg'
        send_text_message(event.reply_token, get_button_die(img_url, "突然有卡車切進去，在台南還敢走路緣啊，人生登出"))
        self.die(event)

    #walk to street
    def is_going_to_street(self, event):
        text = event.message.text
        return text.lower() == "騎樓" or text.lower() == "人行道"

    def on_enter_street(self, event):
        button_message = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://miro.medium.com/max/2686/1*EufFAXj0kLomstftPwP4Cg.png',
                title='此時路過市集，突然有女生大喊「帥哥」~~',
                text='Please select',
                actions=[
                    MessageAction(
                        label='帥爆 回頭',
                        text='帥爆'
                    ),
                    MessageAction(
                        label='不理她',
                        text='不理她'
                    ),
                ]
            )
        )
        send_text_message(event.reply_token, button_message)

    #street to handsome
    def is_going_to_handsome(self, event):
        text = event.message.text
        return text.lower() == "帥爆 回頭" or text.lower() == "帥爆" or text.lower() == "回頭"

    def on_enter_handsome(self, event):
        img_url = 'https://www.teepr.com/wp-content/uploads/2017/09/rer43Ya-3.jpg'
        send_text_message(event.reply_token, get_button_die(img_url, "近女色 失敗", "結果只是個大媽叫你\n被她纏上導致遲到"))
        self.die(event)

    #street to noRespon
    def is_going_to_noRespon(self, event):
        text = event.message.text
        return text.lower() == "不理他" or text.lower() == "不理她"

    def on_enter_noRespon(self, event):
        button_message = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://cdn2.ettoday.net/images/2902/d2902755.jpg',
                title='到了馬路口，遇到紅燈，看起來四周無車',
                text='Please select',
                actions=[
                    MessageAction(
                        label='等紅燈',
                        text='等紅燈'
                    ),
                    MessageAction(
                        label='衝過去',
                        text='衝過去'
                    ),
                ]
            )
        )
        send_text_message(event.reply_token, button_message)

    #noRespon to waitsign
    def is_going_to_waitsign(self, event):
        text = event.message.text
        return text.lower() == "等紅燈"

    def on_enter_waitsign(self, event):
        img_url = 'https://blog.proclaimonline.com/files/2013/07/running-late-630x471.jpg'
        send_text_message(event.reply_token, get_button_die(img_url, "小孩子才走路", "乖乖等紅燈，但已經遲到了"))
        self.die(event)

    #noRespon to rush
    def is_going_to_rush(self, event):
        text = event.message.text
        return text.lower() == "衝過去"

    def on_enter_rush(self, event):
        img_url = 'https://n.sinaimg.cn/translate/199/w600h399/20180610/dPIB-hcufqif3035134.jpg'
        send_text_message(event.reply_token, get_button_die(img_url, "加速跑過去，結果就撞車了，在台南還敢闖紅燈啊"))
        self.die(event)
    

    ############################### big branch ####################################
    #bike to straight
    def is_going_to_straight(self, event):
        text = event.message.text
        return text.lower() == "直走" or text.lower() == "右邊"

    def on_enter_straight(self, event):
        button_message = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.insurancejournal.com/app/uploads/2018/06/crossroad-580x466.jpg',
                title='騎對了方向，再選條路吧~',
                text='Please select',
                actions=[
                    MessageAction(
                        label='馬路',
                        text='馬路'
                    ),
                    MessageAction(
                        label='騎樓',
                        text='騎樓'
                    ),
                    MessageAction(
                        label='路緣',
                        text='路緣'
                    ),
                ]
            )
        )
        send_text_message(event.reply_token, button_message)

    #bike to left
    def is_going_to_left(self, event):
        text = event.message.text
        return text.lower() == "左邊"

    def on_enter_left(self, event):
        img_url = 'https://i.ytimg.com/vi/2stz2Rf98KE/maxresdefault.jpg'
        send_text_message(event.reply_token, get_button_die(img_url, "迷路啦，乖乖遲到吧"))
        self.die(event)

    #straight to road
    def is_going_to_road(self, event):
        text = event.message.text
        return text.lower() == "馬路"

    def on_enter_road(self, event):
        button_message = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://img.letsplay.tw/uploads/20180821145632_79.jpg',
                title='騎一騎肚子餓了，騎到早餐店，買什麼早餐?',
                text='Please select',
                actions=[
                    MessageAction(
                        label='現成的三明治',
                        text='現成的三明治'
                    ),
                    MessageAction(
                        label='現煎的蘿蔔糕',
                        text='現煎的蘿蔔糕'
                    ),
                    MessageAction(
                        label='現成的蛋餅',
                        text='現成的蛋餅'
                    ),
                ]
            )
        )
        send_text_message(event.reply_token, button_message)
    
    #straight to pavement
    def is_going_to_pavement(self, event):
        text = event.message.text
        return text.lower() == "騎樓"

    def on_enter_pavement(self, event):
        img_url = 'https://i0.wp.com/twstreetcorner.org/wp-content/uploads/2015/05/img_3326.jpg?ssl=1'
        send_text_message(event.reply_token, get_button_die(img_url, "台南的騎樓怎麼可能是空的呢，早就推滿東西啦"))
        self.die(event)

    #road to sandwich
    def is_going_to_sandwich(self, event):
        text = event.message.text
        return text.lower() == "現成的三明治" or text.lower() == "三明治" or text.lower() == "現成的蛋餅"

    def on_enter_sandwich(self, event):
        button_message = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://img.news.ebc.net.tw/EbcNews/news/2019/09/23/1569234519_58951.jpg',
                title='買完離開早餐店，終於快到系館了，遭遇了紅燈',
                text='Please select',
                actions=[
                    MessageAction(
                        label='等紅燈',
                        text='等紅燈'
                    ),
                    MessageAction(
                        label='高雄式左轉',
                        text='高雄式左轉'
                    ),
                    MessageAction(
                        label='台南式右轉',
                        text='台南式右轉'
                    ),
                    MessageAction(
                        label='怒燒',
                        text='怒燒'
                    ),
                ]
            )
        )
        send_text_message(event.reply_token, button_message)
    
    #road to radish
    def is_going_to_radish(self, event):
        text = event.message.text
        return text.lower() == "現煎的蘿蔔糕" or text.lower() == "蘿蔔糕"

    def on_enter_radish(self, event):
        img_url = 'https://blog.proclaimonline.com/files/2013/07/running-late-630x471.jpg'
        send_text_message(event.reply_token, get_button_die(img_url, "早餐店煎太久，遲到啦啦啦"))
        self.die(event)

    #sandwich to kaohsiung
    def is_going_to_kaohsiung(self, event):
        text = event.message.text
        return text.lower() == "高雄式左轉" or text.lower() == "高雄" or text.lower() == "左轉"

    def on_enter_kaohsiung(self, event):
        img_url = 'https://img.ltn.com.tw/Upload/news/600/2019/09/05/2906740_1_1.jpg'
        send_text_message(event.reply_token, get_button_die(img_url, '這裡可是台南欸!，直接撞上另一台橫向跨越馬路的車'))
        self.die(event)

    #sandwich to FFF
    def is_going_to_FFF(self, event):
        text = event.message.text
        return text.lower() == "怒燒" or text.lower() == "fff"

    def on_enter_FFF(self, event):
        button_message = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.ytimg.com/vi/YM371GfSe1c/maxresdefault.jpg',
                title='成功消滅一對情侶!',
                text='但似乎不合法\n通過SL大法再來一次',
                actions=[
                    MessageAction(
                        label='走路',
                        text='走路'
                    ),
                    MessageAction(
                        label='機車',
                        text='機車'
                    ),
                    MessageAction(
                        label='腳踏車',
                        text='腳踏車'
                    ),
                ]
            )
        )
        send_text_message(event.reply_token, button_message)
        self.burn_fff()
    
    #sandwich to tainan
    def is_going_to_tainan(self, event):
        text = event.message.text
        return text.lower() == "台南式右轉" or text.lower() == "台南" or text.lower() == "右轉" or text.lower() == "等紅燈"

    def on_enter_tainan(self, event):
        button_message = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://imgur.com/ZMqn2yD.png',
                title='到了地停前，發現旁邊的正妹東西掉了，你應該?',
                text='請勿想歪',
                actions=[
                    MessageAction(
                        label='提醒他',
                        text='提醒他'
                    ),
                    MessageAction(
                        label='撿走',
                        text='撿走'
                    ),
                    MessageAction(
                        label='不理她',
                        text='不理她'
                    ),
                ]
            )
        )
        send_text_message(event.reply_token, button_message)

    #tainan to remind
    def is_going_to_remind(self, event):
        text = event.message.text
        return text.lower() == "提醒他" or text.lower() == "提醒她"

    def on_enter_remind(self, event):
        button_message = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/0bRwX17.jpg',
                title='Happy End，雖然遲到了，但得到了正妹的line',
                text='恭喜通關~\n輸入\"start\"可再來一次',
                actions=[
                    MessageAction(
                        label='Start',
                        text='start'
                    ),
                    MessageAction(
                        label='No Start',
                        text='back'
                    ),
                ]
            )
        )
        send_text_message(event.reply_token, button_message)
        self.happy(event)

    #tainan to pickup
    def is_going_to_pickup(self, event):
        text = event.message.text
        return text.lower() == "撿" or text.lower() == "撿走"

    def on_enter_pickup(self, event):
        img_url = 'https://i.ytimg.com/vi/cR1m7i6srmk/hqdefault.jpg'
        send_text_message(event.reply_token, get_button_die(img_url, "私藏時被抓包，警察局見"))
        self.die(event)

    #tainan to noRemind
    def is_going_to_noRemind(self, event):
        text = event.message.text
        return text.lower() == "不理他" or text.lower() == "不理她"

    def on_enter_noRemind(self, event):
        button_message = TemplateSendMessage(
            alt_text='Button',
            template=ButtonsTemplate(
                thumbnail_image_url='https://vthumb.ykimg.com/054101015B9681B48B7B44A3A3525E01',
                title='True End，準時抵達教室，上課囉',
                text='恭喜通關~\n輸入\"start\"可再來一次',
                actions=[
                    MessageAction(
                        label='Start',
                        text='start'
                    ),
                    MessageAction(
                        label='No Start',
                        text='back'
                    ),
                ]
            )
        )
        send_text_message(event.reply_token, button_message)
        self.happy(event)