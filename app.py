import telebot
from config import MY_TOKEN, keys
from extensions import Converter, ConvertionException, UserDB


bot = telebot.TeleBot(MY_TOKEN)

vals = {
    1: ('RUB', 'EUR')
}

db = UserDB()


@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = '''Чтобы начать работу введите команду /set \n
    По умолчанию идет конвертация евро в рубль\n
    После выбора валюты введите количество'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['set'])
def sett(message):
    markup = telebot.types.InlineKeyboardMarkup()
    for vol, form in keys.items():
        button = telebot.types.InlineKeyboardButton(text=vol.capitalize(), callback_data=f'val1 {form}')
        markup.add(button)

    bot.send_message(chat_id=message.chat.id, text='Выберите валюту, из которой будем конвертировать', reply_markup=markup)

    markup = telebot.types.InlineKeyboardMarkup()
    for vol, form in keys.items():
        button = telebot.types.InlineKeyboardButton(text=vol.capitalize(), callback_data=f'val2 {form}')
        markup.add(button)

    bot.send_message(chat_id=message.chat.id, text='Выберите валюту, в которую будем конвертировать', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    t, st = call.data.split()
    user_id = call.message.chat.id
    if t == 'val1':
        db.change_from(user_id, st)
    if t == 'val2':
        db.change_to(user_id, st)
    pair = db.get_pair(user_id)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=f'Теперь конвертируем из {pair[0]} в {pair[1]}')


@bot.message_handler(content_types=['text'])
def converter(message):
    pair = db.get_pair(message.chat.id)
    values = [*pair, message.text.strip()]
    try:

        total = Converter.get_price(values)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {values[2]} {values[0]} в {values[1]} - {total}{pair[1]}'
        bot.reply_to(message, text)


bot.polling()
