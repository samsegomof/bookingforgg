import telebot

from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

TOKEN = '5558041471:AAFVW_M7z7Biqv0pCjjKSFB8dZC5urKiOxM'

bot = telebot.TeleBot(TOKEN)


"""Create a buttons"""


def get_reply_keyboard(buttons):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for button in buttons:
        keyboard.add(KeyboardButton(button))

    return keyboard


info_btn = '🎮 Подробнее'
price_btn = '💳 Прайс'
booking_btn = '🕒 Забронировать'
back_btn = '🔙 Назад 🔙'
reviews_btn = '📢 Отзывы'
kitchen_btn = '🍽️ Наша кухня'

about_us = 'Мы рады приветствовать вас! Это бот-помощник GoodGameClub!\n' \
           'У нас вы можете отлично провести время за любимыми играми на консолях:\nPS4, PS5, XBox X, VR, SEGA\n'\
           'Посмотреть любимые спортивные трансляции на большом экране и отведать наше оригинальное меню.\n' \
           'Отпраздновать ваше событие или День Рождения вашего ребенка!\n'\
           'Так же вы можете забронировать VIP комнату для отдыха с друзьями!\n'\
           'Режим работы круглосуточно, кухня с 10:00 до 22:00\n'\
           'Если у вас возникли вопросы напишите нам в телеграмм @Garry_Good\n' \
           'или позвоните по номеру +7 961 364-12-78 или +7 905 007-90-22\n'\
           'Для того чтобы узнать цены перейдите в раздел - \n💳 Прайс.\n' \
           'Для бронирования нажмите - \n🕒 Забронировать.\n'\
           'Ознакомиться с меню нашей кухни нажмите -\n🍽️ Наша кухня\n'\
           'Оставить отзыв и предложения по улучшению нажмите на - \n📢 Отзывы\n'


start_msg = f"""GoodGameCafeBot - Бот игрового кафе!\nЧтобы узнать подробнее перейдите в раздел {info_btn}"""

booking_msg = "Для брони стола нажмите"
price_msg = "Для просмотра нашего прайса нажмите на"
reviews_msg = "Уважаемый клиент! Нам важно ваше мнение, пожалуйста перейдите по ссылке"
error_msg = "Я не понимаю о чем ты!\nВозвращаю тебя в главное меню."
kitchen_msg = "Ознакомиться с меню нашей кухни тут"


@bot.message_handler(commands=['start'])
def start_func(message):
    bot.send_message(message.chat.id, f'Привет 🤝 {message.from_user.first_name} 🤝 !\n{start_msg}',
                     reply_markup=get_reply_keyboard([info_btn]))


@bot.message_handler(content_types='text')
def main_menu(message):
    answer = message.text
    commands_list = [info_btn, booking_btn, back_btn, price_btn, reviews_btn, kitchen_btn]

    if answer == info_btn:
        bot.send_message(message.chat.id, about_us, reply_markup=get_reply_keyboard([price_btn,
                                                                                     booking_btn,
                                                                                     back_btn, reviews_btn, kitchen_btn]))
    if answer == booking_btn:
        keyboard = InlineKeyboardMarkup()
        url_button = InlineKeyboardButton(text=booking_btn, url="https://goodgame-ufa.herokuapp.com/booking/new")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, f"{booking_msg}\n{booking_btn}.", reply_markup=keyboard)
    if answer == back_btn:
        bot.send_message(message.chat.id, f'Привет 🤝 {message.from_user.first_name} 🤝 !\n{start_msg}',
                         reply_markup=get_reply_keyboard([info_btn]))

    if answer == price_btn:
        #keyboard = InlineKeyboardMarkup()
        #url_button = InlineKeyboardButton(text=price_btn, url="https://telegra.ph/Nash-prajs-06-12-2")
        #keyboard.add(url_button)
        #bot.send_message(message.chat.id, f"{price_msg}\n{price_btn}.", reply_markup=keyboard)
        bot.send_photo(message.chat.id, photo=open('tmp/img/game_menu.jpg', 'rb'))

    if answer == reviews_btn:
        keyboard = InlineKeyboardMarkup()
        url_button = InlineKeyboardButton(text=reviews_btn, url="https://forms.gle/zmLoxGQoKz8bnqVx6")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, f"{reviews_msg}\n{reviews_btn}.", reply_markup=keyboard)

    if answer == kitchen_btn:
        #keyboard = InlineKeyboardMarkup()
        #url_button = InlineKeyboardButton(text=kitchen_btn, url="https://telegra.ph/Menyu-kuhni-06-23")
        #keyboard.add(url_button)
        #bot.send_message(message.chat.id, f"{kitchen_msg}.", reply_markup=keyboard)
        bot.send_photo(message.chat.id, photo=open("tmp/img/menu_kitchen1.jpg", "rb"))
        bot.send_photo(message.chat.id, open("tmp/img/menu_kitchen2.jpg", "rb"))
        bot.send_photo(message.chat.id, open("tmp/img/child_menu.jpg", "rb"))

    if answer not in commands_list:
        bot.send_message(message.chat.id, error_msg)
        bot.send_message(message.chat.id, f'Привет 🤝 {message.from_user.first_name} 🤝 !\n{start_msg}',
                         reply_markup=get_reply_keyboard([info_btn]))


if __name__ == "__main__":
    bot.polling(none_stop=True)
