import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('1894004415:AAFA6kitrRztb2YXVHSLl-XBy2OqbvMOr4Y')

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

flag_5x20 = ''
flag_20x40 = ''
flag_40x70 = ''


number = ''
h_or_d = ''
home = ''
ylisa = ''


user_list = []




@bot.message_handler(content_types=["text"])
def find_item(message):
    user_list.clear()


    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("5x20")
        item2 = types.KeyboardButton("20x40")
        item3 = types.KeyboardButton("40x70")
        markup.add(item1, item2, item3)

        us_s = message.from_user.first_name

        bot.send_message(message.chat.id, 'Здравствуйте, ' + us_s + ', выберите понравившиеся Вами вариант',
                        reply_markup=markup)
        bot.register_next_step_handler(message, item_markup)


@bot.message_handler(content_types=['text'])
def item_markup(message):
    markup_for_all = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = types.KeyboardButton('Да!')
    no = types.KeyboardButton('Нет')
    markup_for_all.add(yes, no)

    if message.text == '5x20':
        bot.send_message(message.chat.id,
                         'Отлично!😊  Цена выбранного вами тарифа составляет 510 рублей. Вы готовы оплатить эту цену?',
                         reply_markup=markup_for_all)

        flag_5x20 = '5x20'
        user_list.append(flag_5x20)

        bot.register_next_step_handler(message, yes_or_no)



    elif message.text == '20x40':
        bot.send_message(message.chat.id,
                         'Отлично!😊  Цена выбранного вами тарифа составляет 350 рублей. Вы готовы оплатить эту цену?',
                         reply_markup=markup_for_all)

        flag_20x40 = '20x40'
        user_list.append(flag_20x40)

        bot.register_next_step_handler(message, yes_or_no)

    elif message.text == '40x70':
        bot.send_message(message.chat.id,
                         'Отлично!😊  Цена выбранного вами тарифа составляет 400 рублей. Вы готовы оплатить эту цену?',
                         reply_markup=markup_for_all)

        flag_40x70 = '40x70'
        user_list.append(flag_40x70)

        bot.register_next_step_handler(message, yes_or_no)


def yes_or_no(message):
    if message.text == 'Да!':
        bot.send_message(message.chat.id, 'Отлично! Теперь Вам нужно пройти небольшую анкету')
        bot.send_message(message.chat.id, 'Как вас зовут?(ФИО)')
        bot.register_next_step_handler(message, fio)


    elif message.text == 'Нет':
        user_list.clear()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("5x20")
        item2 = types.KeyboardButton("20x40")
        item3 = types.KeyboardButton("40x70")
        markup.add(item1, item2, item3)

        us_s = message.from_user.first_name

        bot.send_message(message.chat.id, 'Здравствуйте, ' + us_s + ', выберите понравившиеся Вами вариант',
                         reply_markup=markup)
        bot.register_next_step_handler(message, item_markup)





def fio(message):
    name = str(message.text)


    counter = 0
    for i in name:
        if chr(32) == i:
            counter += 1

    if counter >= 3 or counter <= 1:
        bot.send_message(message.chat.id, 'Введите Ваше настоящее ФИО')
        user_list.append(name)
        bot.register_next_step_handler(message, fio)

    else:
        user_list.append(name)
        bot.send_message(message.chat.id,
                         'Хорошо, теперь введите ваш номер, чтобы с вами связаться. Вводите в формате +7, иначе не заявка не будет принята')
        bot.register_next_step_handler(message, number_f)



def number_f(message):
    number = str(message.text)
    count = 12
    count_user_number = 0



    for i in number:
        count_user_number += 1

    flag = False
    for i in number:
        if chr(43) <= i <= chr(57):
            flag = True


    if number[0] != '+':
        bot.send_message(message.chat.id, 'Введите Ваш настоящий номер')
        bot.register_next_step_handler(message, number_f)

    elif count_user_number != count:
        bot.send_message(message.chat.id, 'Введите Ваш настоящий номер')
        bot.register_next_step_handler(message, number_f)



    elif flag == True:
        user_list.append(number)
        markup_for_d_or_s = types.ReplyKeyboardMarkup(resize_keyboard=True)
        s = types.KeyboardButton('Самовызов')
        d = types.KeyboardButton('Доставка')
        markup_for_d_or_s.add(s, d)

        bot.send_message(message.chat.id, 'Как вы будите забирать заказ?', reply_markup=markup_for_d_or_s)
        bot.register_next_step_handler(message, home_or_samo)


    elif flag == False:
        bot.send_message(message.chat.id, 'Введите Ваш настоящий номер')
        bot.register_next_step_handler(message, number_f)

    else:
        bot.send_message(message.chat.id, 'Введите Ваш настоящий номер')
        bot.register_next_step_handler(message, number_f)


def home_or_samo(message):

    if message.text == 'Самовызов':
        ulisa = ''
        user_list.append(ulisa)
        h_or_d = 'Самовызов'
        user_list.append(h_or_d)
        bot.send_message(message.chat.id, 'Ваша заявка принята!')
        us_id = message.from_user.id
        print(user_list)

        cursor.execute(
            "INSERT INTO login_id VALUES (?, ?, ?, ?, ?, ?)", (us_id, user_list[1], user_list[2], user_list[4],
                                                                     user_list[3], user_list[0]))
        conn.commit()

    elif message.text == 'Доставка':
        bot.send_message(message.chat.id, 'Введите адрес:')

        h_or_d = 'Доставка'
        user_list.append(h_or_d)

        bot.register_next_step_handler(message, text)


def text(message):
    us_id = message.from_user.id
    ulisa = str(message.text)
    user_list.append(ulisa)
    print(user_list)

    cursor.execute(
        "INSERT INTO login_id VALUES (?, ?, ?, ?, ?, ?)", (us_id, user_list[1], user_list[2], user_list[3],
                                                             user_list[4],
                                                             user_list[0]))
    conn.commit()

    bot.send_message(message.chat.id, 'Ваша заявка принята')



bot.polling(none_stop=True)
