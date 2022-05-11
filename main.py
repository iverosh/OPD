from profiles import *



@bot.message_handler(content_types=['text'])
def start(message):
    id = int(message.chat.id)
    search_res = db_manager.search_user(conn, id)
    if (search_res == 0):
        db_manager.add_active_user(conn, id, 'null', 0, '/stop')
    if (db_manager.is_logged(conn, id)):
        if (search_res[6] == "ADMIN"):
            admin(message, id, search_res)
        if (search_res[6] == "TECHNOLOGIST"):
            technologist(message, id, search_res)
        if (search_res[6] == "BRIGADIER"):
            brigadier(message, id, search_res)



    else:
        passwords = db_manager.get_passwords(conn)
        if (db_manager.is_tried_to_log(conn, id) == 0):
            bot.send_message(message.chat.id,
                             'Введите пароль. В целях Вашей же безопасности сообщения с вводами пароля будут удалены.')
            db_manager.update_tried_to_log(conn, id, 'true')
        elif (message.text == passwords[0][0]):
            db_manager.update_log_in(conn, id, 'true')
            bot.send_message(message.chat.id,
                             'Пароль успешно введен.\nВы- Администратор\nДля запуска напишите /start\nДля остановки напишите /stop\nДля выхода из учетной записи напишите /logout\nЧтобы сменить пароль напишите /changepass')
            bot.delete_message(message.chat.id, message.message_id)
            db_manager.update_profile_type(conn, id, "ADMIN")
        elif (message.text == passwords[1][0]):
            db_manager.update_log_in(conn, id, 'true')
            bot.send_message(message.chat.id,
                             'Пароль успешно введен.\nВы- Технолог\nДля запуска напишите /start\nДля остановки напишите /stop\nДля выхода из учетной записи напишите /logout')

            bot.delete_message(message.chat.id, message.message_id)
            db_manager.update_profile_type(conn, id, "TECHNOLOGIST")
        elif (message.text == passwords[2][0]):
            db_manager.update_log_in(conn, id, 'true')
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(id, "Пароль успешно введен")
            db_manager.update_profile_type(conn, id, "BRIGADIER")

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            Hanky_btn = types.KeyboardButton("HANKY")
            Facial_btn = types.KeyboardButton("FACIAL")
            markup.add(Hanky_btn, Facial_btn)
            bot.send_message(message.chat.id,
                             'Выберите линию, на которой вы работаете',
                             reply_markup=markup)

        else:
            bot.send_message(message.chat.id, 'Неверный пароль, попробуйте еще раз')
            bot.delete_message(message.chat.id, message.message_id)
if (__name__ == '__main__'):
    try:
        db_manager.create_table_comments(conn)
        db_manager.create_table_users(conn)
        db_manager.create_table_targets(conn)
        db_manager.create_table_passwords(conn)
        bot.polling(none_stop=True)
    except:
        pass
    finally:
        conn.close()