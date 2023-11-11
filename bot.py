#by: @F_E_Y
#in: 2023/11/11
#channel: @Se7en_Eyes
import subprocess
import os
import re
if not os.path.isdir('data'):
    os.mkdir('data')
try:
    from telebot import telebot
    from telebot.types import InlineKeyboardButton as btn
    from telebot.types import InlineKeyboardMarkup as mk
    from telebot.types import KeyboardButton as kb
    from telebot.types import ReplyKeyboardMarkup as rep
    from telebot.types import InlineKeyboardButton as btn
    from telebot.types import InlineKeyboardMarkup as mk
    from telebot.types import KeyboardButton as kb
    from telebot.types import ReplyKeyboardMarkup as rep
    from kvsqlite.sync import Client
    import requests

admin = "6673736816" #your tele ID
token = Config.TG_BOT_TOKEN #bot token
domain = "smmmain.com" #domain site
api_key = "4fd47e2120255af9f105804e62d19f81" #Your api key from
id_service = 103

db = Client('data/mody.sql', 'rshq')
bot = TeleBot(token=token,skip_pending=True, parse_mode='html', disable_web_page_preview=True)
print(bot)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    keys = rep(row_width=2, resize_keyboard=True)
    btn1 = kb('طلب رشق جديد 🆕')
    btn2 = kb('قسم الرشق التلقائي 🤓')
    keys.add(btn2, btn1)
    msg = f"""• مرحبا بك عزيزي <a href="tg://user?id={user_id}">{message.from_user.first_name}</a> 👋

<strong>• في بوت رشق المشاهدات المجاني 👀🆓</strong>

• اختر ماتود فعلة من الازرار ادناه 📥"""
    bot.reply_to(message, msg, reply_markup=keys)
    if not db.exists(f"user_{user_id}"):
        db.set(f"user_{user_id}", True)
        members = 0
        users = db.keys('user_%')
        for _ in users:
            members+=1
        if message.from_user.username == None: username = "لا يوجد"
        else: username = "@"+str(message.from_user.username)
        bot.send_message(chat_id=admin, text=f'٭ تم دخول شخص جديد الى البوت الخاص بك 👾\n\n• معلومات العضو الجديد .\n\n• الاسم : <a href="tg://user?id={user_id}">{message.from_user.first_name}</a>\n• المعرف : {username}\n• الايدي : {message.from_user.id}\n\n• عدد الاعضاء الكلي : {members}')
        
        
@bot.message_handler(func=(lambda message: True))
def msgs(message):
    text = message.text
    user_id = message.from_user.id
    keys = rep(row_width=2, resize_keyboard=True)
    btn1 = kb('رجوع')
    keys.add(btn1)
    if text == "طلب رشق جديد 🆕":
        step = bot.reply_to(message, "• ارسل رابط المنشور الذي تود رشقه", reply_markup=keys)
        bot.register_next_step_handler(step, link_post)
    elif text == "قسم الرشق التلقائي 🤓":
        keys = rep(row_width=2, resize_keyboard=True)
        btn1 = kb('اضف قناة ➕')
        btn2 = kb('حذف قناة 🗑')
        btn3 = kb('رجوع')
        keys.add(btn2, btn1)
        keys.add(btn3)
        bot.reply_to(message, "قسم الرشق التلقائي 🤓", reply_markup=keys)
    elif text == "رجوع":
        keys = rep(row_width=2, resize_keyboard=True)
        btn1 = kb('طلب رشق جديد 🆕')
        btn2 = kb('قسم الرشق التلقائي 🤓')
        keys.add(btn2, btn1)
        msg = f"""• مرحبا بك عزيزي <a href="tg://user?id={user_id}">{message.from_user.first_name}</a> 👋

<strong>• في بوت رشق المشاهدات المجاني 👀🆓</strong>

• اختر ماتود فعلة من الازرار ادناه 📥"""
        bot.reply_to(message, msg, reply_markup=keys)
    elif text == "اضف قناة ➕":
        chat = bot.get_me()
        username = chat.username
        keys = mk()
        btn1 = btn("رفع البوت مشرف في قناة 📢", url=f"https://t.me/{username}/?startchannel=true")
        keys.add(btn1)
        msg = f"""<strong>• ارفع البوت @{username} ادمن في قناتك ثم ارسل رابط او معرف قناتك 🔗</strong>

• او يمكنك الضغط علي الزر ادناه ثم اختر القناة التي تريد اضافتها📥"""
        step = bot.reply_to(message, msg, reply_markup=keys)
        bot.register_next_step_handler(step, add_channel)
    elif text == "حذف قناة 🗑":
        step = bot.reply_to(message, "• ارسل الان معرف او رابط القناة التي تريد حذفها")
        bot.register_next_step_handler(step, del_channel)
    
@bot.channel_post_handler(func=(lambda message: True))
def channels_msgs(message):
    username = message.chat.username.lower()
    print(username)
    if db.exists(username):
        msg_id = message.message_id
        url = f"https://t.me/{username}/{msg_id}"
        response = requests.get(f"https://{domain}/api/v2?key={api_key}&action=add&service={id_service}&quantity=100&link={url}")
        if response.status_code == 200:
            try:
                order = response.json()['order']
                id = db.get(username)['id']
                keys = mk()
                btn1 = btn("رابط المنشور 🔗", url=url)
                keys.add(btn1)
                db.set(url, True)
                msg = f"""تم بدء الرشق بنجاح ✅

العدد : 1000 مشاهدة
ايدي الطلب : {order}
الرابط : {url}

<strong>• ملحوظه سرعه الرشق ليست قوية بما يكفي ، اذا قد تم طلب رشق من قبل لهذا المنشور لن يتم تنفيذ طلبك </strong>""" 
                bot.send_message(chat_id=int(id), text=msg, reply_markup=keys)
            except Exception as a:
            	print(a)
            	return



def format_post(link):
    body = r"https?://t\.me/(\w+)/(\d+)"
    if re.match(body, link):
        return True
    else:
        return False
        
def format_link(link):
    body = r"https:\/\/t.me\/[a-zA-Z0-9_]{5,32}$"
    if re.match(body, link):
        return True
    else:
        return False
        
def link_post(message):
     text = message.text
     if text == "رجوع":
        msgs(message)
        return
     check_post = format_post(text)
     if not check_post:
        bot.reply_to(message, "• الرابط غير صحيح ، تاكد من صحة الرابط اولاً")
        return
     response = requests.get(f"https://{domain}/api/v2?key={api_key}&action=add&service={id_service}&quantity=1000&link={text}")
     if db.exists(text):
        bot.reply_to(message, "• عذرا، تم طلب رشق لهذا المنشور من قبل")
        return
     if response.status_code == 200:
        try:
            order = response.json()['order']
            msg = f"""تم بدء الرشق بنجاح ✅

العدد : 1000 مشاهدة
ايدي الطلب : {order}
الرابط : {text}

<strong>• ملحوظه سرعه الرشق ليست قوية بما يكفي ، اذا قد تم طلب رشق من قبل لهذا المنشور لن يتم تنفيذ طلبك </strong>"""
            bot.reply_to(message, msg)
            db.set(text, True)
        except:
            bot.reply_to(message, "• حدث خطا ما ، تواصل مع المطور لحل المشكلة")
     else: bot.reply_to(message, "• حدث خطا ما ، تواصل مع المطور لحل المشكلة")
        
def add_channel(message):
    text = message.text
    if text == "رجوع":
        msgs(message)
        return
    check_link = format_link(text)
    if not check_link:
        bot.reply_to(message, "• الرابط غير صحيح ، تاكد من صحة الرابط اولاً")
        return
    channel = text.replace("https://t.me/", "").replace("@", "").lower()
    data = {'channel': channel, 'id': message.from_user.id}
    db.set(channel.lower(), data)
    bot.reply_to(message, "• تم حفظ القناة بنجاح ✅")

def del_channel(message):
    text = message.text
    if text == "رجوع":
        msgs(message)
        return
    check_link = format_link(text)
    if not check_link:
        bot.reply_to(message, "• الرابط غير صحيح ، تاكد من صحة الرابط اولاً")
        return
    channel = text.replace("https://t.me/", "").replace("@", "").lower()
    if db.exists(channel):
        id = db.get(channel)['id']
        if int(message.from_user.id) != int(id):
            bot.reply_to(message, "• عذرا، انت لم تقم باضافة هذه القناة")
            return
        db.delete(channel)
        bot.reply_to(message, "• تم حذف القناة بنجاح 🗑")
    else: bot.reply_to(message, "• عذرا، انت لم تقم باضافة هذه القناة")
    
bot.infinity_polling()

#by: @F_E_Y
#in: 2023/11/11
#channel: @Se7en_Eyes
