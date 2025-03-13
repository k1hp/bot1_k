import telebot
from telebot import types
from others.conf import TOKEN

bot = telebot.TeleBot(TOKEN)
SETTINGS = ("Username", "ID", "Lastname", "Premium")


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.reply_to(message, "Привет, нефор!")


@bot.message_handler(commands=['buttons'])
def button_message(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = []
    for item_name in SETTINGS:
        items.append(types.KeyboardButton(item_name))
    markup.add(*items)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types=['text', 'sticker'])
def get_response(message: types.Message):
    commands = dict(zip(SETTINGS, (
    message.from_user.first_name, message.from_user.id, message.from_user.last_name, message.from_user.is_premium)))
    if message.text in commands:
        bot.send_message(message.chat.id,
                         f"Your `{message.text}` is {commands[message.text] if commands[message.text] is not None else 'not exists!'}")
    else:
        bot.send_message(message.chat.id, message.sticker.emoji)

    print(message)


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
