import telebot
import sqlite3

bot = telebot.TeleBot('1880576160:AAH4ia98szT25Eh4zZwGdROh6fCLYKRwzds')

conn = sqlite3.connect('users.db', check_same_thread=False)

list_user = []

with conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM login_id")
    rows = cur.fetchall()

    for row in rows:
        list_user.append(row)


password_valid = 'Shamil7825'

name =''



@bot.message_handler(content_types=["text"])
def password(message):
        bot.send_message(message.chat.id, 'Введите пароль')
        bot.register_next_step_handler(message, check_password)


@bot.message_handler(content_types=["text"])
def check_password(message):
    password_write_username = str(message.text)

    if password_write_username == password_valid:
       for i in range(len(rows)):
           bot.send_message(message.chat.id, 'id: ' + str(rows[i][0]) + '\n' + 'fio: ' + str(rows[0][1]) + '\n' + 'number: ' +
                            str(rows[i][2]) + ' \n' + 'type of delivery: ' + str(rows[i][3]) + ' \n' + 'street: ' + str(rows[i][4]) +
                            '\n' + 'item: ' + str(rows[i][5]) + '\n')





    else:
        password(message)



bot.polling(none_stop=True)




