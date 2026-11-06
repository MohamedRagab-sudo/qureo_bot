import telebot
from telebot import types

TOKEN = "9076457407:AAE4TEDU2Tm8XsHi0YIvz7A0a3lIwCqyqB0"
OWNER_USERNAME = "x_elmoksh711_x"
bot = telebot.TeleBot(TOKEN)

PAID_USERNAMES = {"x_abdo_x211"} # اللي هيدفع هتزوده هنا
ADMIN_USERNAME = "x_elmoksh711_x" # انت - كل حاجة مفتوحة عندك

# هنا هنحط الفصول - لما تبعتلي سكرين لفصل هملاهولك بالظبط
CHAPTERS = {}
# بنعمل 42 فصل فاضيين الاول عشان البوت ميقفش
for i in range(1, 43):
    CHAPTERS[i] = {
        "title": f"الفصل {i}",
        "summary": "لسه هنحط شرح المنصة هنا - ابعت سكرين للفصل ده",
        "code": "// لسه هنحط مثال المنصة هنا",
        "quiz": "ابعت سكرين للسؤال بتاع الفصل ده وهنحط الشرح والاجابة هنا"
    }

# دي الفصول اللي احنا متأكدين منها من QUREO
CHAPTERS[1] = {"title": "الفصل 1: يعني ايه برمجة؟", "summary": "البرمجة هي اوامر بنكتبها للكمبيوتر. في QUREO بنستخدم JavaScript", "code": "console.log('Hello QUREO')", "quiz": "بنطبع ازاي في QUREO؟\nأ) console.log\nب) print"}
CHAPTERS[2] = {"title": "الفصل 2: العمليات الحسابية", "summary": "الجمع + والطرح - والضرب * والقسمة /", "code": "console.log(19 + 40)\nconsole.log(7 - 2)", "quiz": "ناتج 19 + 40 = 59"}

def chapters_keyboard(username=None):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    for i in range(1, 43):
        # انت كأدمن كل حاجة مفتوحة عندك
        # من 1 لـ 30 مجاني للكل
        # من 31 لـ 42 للمشتركين بس
        if i <= 30 or username in PAID_USERNAMES or username == ADMIN_USERNAME:
            buttons.append(types.InlineKeyboardButton(f"{i} ✅", callback_data=f"ch_{i}"))
        else:
            buttons.append(types.InlineKeyboardButton(f"{i} 🔒", callback_data=f"locked_{i}"))
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    text = "اهلا بيك في بوت QUREO 🎓\n\n✅ من 1 لـ 30 مجاني\n🔒 من 31 لـ 42 باشتراك\n\nاختار فصل:"
    bot.send_message(message.chat.id, text, reply_markup=chapters_keyboard(message.from_user.username))

@bot.callback_query_handler(func=lambda call: call.data.startswith('ch_'))
def open_chapter(call):
    num = int(call.data.split('_')[1])
    ch = CHAPTERS[num]
    text = f"📚 {ch['title']}\n\n📝 الشرح:\n{ch['summary']}\n\n💻 مثال كود:\n`{ch['code']}`\n\n❓ سؤال:\n{ch['quiz']}"
    bot.send_message(call.message.chat.id, text, parse_mode='Markdown', reply_markup=chapters_keyboard(call.from_user.username))
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('locked_'))
def locked(call):
    num = call.data.split('_')[1]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📩 كلم صاحب البوت للاشتراك", url=f"https://t.me/{OWNER_USERNAME}"))
    markup.add(types.InlineKeyboardButton("🔙 ارجع للفصول", callback_data="back"))
    bot.send_message(call.message.chat.id, f"🔒 الفصل {num} مقفول\n\nللمشتركين بس.", reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back(call):
    bot.send_message(call.message.chat.id, "اختار فصل:", reply_markup=chapters_keyboard(call.from_user.username))

print("QUREO_BOT شغال تمام")
bot.polling()