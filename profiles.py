from utils import *


def admin(message):
    id = int(message.chat.id)
    search_res = db_manager.search_user(conn, id)
    if (search_res == 0):
        db_manager.add_active_user(conn, id, 'null', 0, '/stop')
    if (db_manager.is_logged(conn, id)):
        if (message.text == '/start'):
            if (search_res == 0 or search_res[3] == '/stop'):
                bot.send_message(message.chat.id,
                                 'Вы подписались на рассылку сообщений о результатах работы смены. Теперь вам будут приходить результаты работы выбранной линии в конце каждой рабочей смены. Чтобы отписаться, нажмите /stop.')

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                Hanky_btn = types.KeyboardButton("HANKY")
                Facial_btn = types.KeyboardButton("FACIAL")
                Both_btn = types.KeyboardButton("Обе линии")
                markup.add(Hanky_btn, Facial_btn, Both_btn)
                bot.send_message(message.chat.id, 'Выберите линию.', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Вы уже подписаны на рассылку.')

        elif (message.text == '/stop'):
            if (search_res == 0 or search_res[3] == '/stop'):
                bot.send_message(message.chat.id,
                                 'Вы ни на что не подписаны. Чтобы подписаться на информационную рассылку, нажмите /start.')
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                Hanky_btn = types.KeyboardButton("HANKY")
                Facial_btn = types.KeyboardButton("FACIAL")
                Both_btn = types.KeyboardButton("Обе линии")
                markup.add(Hanky_btn, Facial_btn, Both_btn)
                bot.send_message(message.chat.id,
                                 'Вы отписались от рассылки. Чтобы подписаться снова, нажмите /start или сразу выберете линию',
                                 reply_markup=markup)
                db_manager.update_status(conn, id, search_res[1], search_res[2], '/stop')
                stop_process(id)

        elif (message.text == '/help'):
            bot.send_message(message.chat.id,
                             'Для запуска напишите /start\nДля остановки напишите /stop\nДля выхода из учетной записи напишите /logout\nДля смены пароля пользователю нажмите /changepass')

        elif (
                message.text == 'HANKY' or message.text == 'FACIAL' or message.text == 'Обе линии' or message.text == 'жопа'):
            if (search_res == 0 or search_res[3] == '/stop'):
                line = message.text
                if (message.text == 'HANKY' or message.text == 'FACIAL' or message.text == 'жопа'):
                    bot.send_message(message.chat.id, f"Вы выбрали линию {line}.")
                    start_process(id, line)
                elif (message.text == 'Обе линии'):
                    bot.send_message(message.chat.id, f"Вы выбрали обе линии.")
                    start_process(id, line)
            else:
                bot.send_message(message.chat.id, 'Вы уже подписаны на рассылку.')

        elif (message.text == '/logout'):

            if (search_res == 0 or search_res[3] == '/stop'):
                db_manager.update_log_in(conn, id, 'false')
                db_manager.update_tried_to_log(conn, id, 'false')
                bot.send_message(message.chat.id,
                                 'Вы вышли из учетной записи. Для повторного входа отправьте любое сообщение.')
            else:
                bot.send_message(message.chat.id,
                                 'Нельзя выйти из учетной записи до завершения процесса рассылки. Для остановки рассылки напишите /stop')

        elif (message.text == '/changepass'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            admin = types.KeyboardButton("Администратору")
            technologist = types.KeyboardButton("Технологу")
            brigadier = types.KeyboardButton("Бригадиру")
            markup.add(admin, technologist, brigadier)
            bot.send_message(message.chat.id, 'Выберите, кому Вы хотите поменять пароль.', reply_markup=markup)

        elif (message.text == "Администратору" or message.text =="Технологу" or message.text == "Бригадиру"):
            if message.text == "Администратору":
                profile_type = "admin"
            if message.text == "Технологу":
                profile_type = "technologist"
            if message.text == "Бригадиру":
                profile_type = "brigadier"
            db_manager.update_changing_pass(conn, profile_type, id)

        elif(search_res[7] != "NO"):
            db_manager.change_pass(conn, search_res[7], message.text)
            db_manager.update_changing_pass(conn, "NO", id)


        else:
            bot.send_message(message.from_user.id, 'Неизвестная команда. Напишите /help')
    else:
        if (db_manager.is_tried_to_log(conn, id) == 0):
            bot.send_message(message.chat.id,
                             'Введите пароль. В целях Вашей же безопасности сообщения с вводами пароля будут удалены.')
            db_manager.update_tried_to_log(conn, id, 'true')
        elif (message.text == password):
            db_manager.update_log_in(conn, id, 'true')
            bot.send_message(message.chat.id,
                             'Пароль успешно введен.\nДля запуска напишите /start\nДля остановки напишите /stop\nДля выхода из учетной записи напишите /logout\nДля смены пароля пользователю нажмите /changepass')
            bot.delete_message(message.chat.id, message.message_id)
        else:
            bot.send_message(message.chat.id, 'Неверный пароль, попробуйте еще раз')
            bot.delete_message(message.chat.id, message.message_id)


def technologist(message):
    id = int(message.chat.id)
    search_res = db_manager.search_user(conn, id)
    if (search_res == 0):
        db_manager.add_active_user(conn, id, 'null', 0, '/stop')
    if (db_manager.is_logged(conn, id)):
        line = search_res[9]
        if (message.text == '/start'):
            if (search_res == 0 or search_res[3] == '/stop'):
                bot.send_message(message.chat.id,
                                 'Вы подписались на рассылку сообщений о результатах работы смены. Теперь вам будут приходить результаты работы выбранной линии в конце каждой рабочей смены. Чтобы отписаться, нажмите /stop.')

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                Hanky_btn = types.KeyboardButton("HANKY")
                Facial_btn = types.KeyboardButton("FACIAL")
                Both_btn = types.KeyboardButton("Обе линии")
                markup.add(Hanky_btn, Facial_btn, Both_btn)
                bot.send_message(message.chat.id, 'Выберите линию.', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Вы уже подписаны на расслыку.')

        elif (message.text == '/stop'):
            if (search_res == 0 or search_res[3] == '/stop'):
                bot.send_message(message.chat.id,
                                 'Вы ни на что не подписаны. Чтобы подписаться на информационную рассылку, нажмите /start.')
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                Hanky_btn = types.KeyboardButton("HANKY")
                Facial_btn = types.KeyboardButton("FACIAL")
                Both_btn = types.KeyboardButton("Обе линии")
                markup.add(Hanky_btn, Facial_btn, Both_btn)
                bot.send_message(message.chat.id,
                                 'Вы отписались от рассылки. Чтобы подписаться снова, нажмите /start или сразу выберете линию',
                                 reply_markup=markup)
                db_manager.update_status(conn, id, search_res[1], search_res[2], '/stop')
                stop_process(id)

        elif (message.text == '/help'):
            bot.send_message(message.chat.id,
                             'Для запуска напишите /start\nДля остановки напишите /stop\nДля выхода из учетной записи напишите /logout\nДля ввода цели на месяц введите /target')

        elif (message.text == 'HANKY' or message.text == 'FACIAL' or message.text == 'Обе линии'):
            if (search_res == 0 or search_res[3] == '/stop'):
                line = message.text
                if (message.text == 'HANKY' or message.text == 'FACIAL'):
                    bot.send_message(message.chat.id, f"Вы выбрали линию {line}.")
                    start_process(id, line)
                elif (message.text == 'Обе линии'):
                    bot.send_message(message.chat.id, f"Вы выбрали обе линии.")
                    start_process(id, line)
            else:
                bot.send_message(message.chat.id, 'Вы уже подписаны на расслыку.')

        elif (message.text == '/logout'):

            if (search_res == 0 or search_res[3] == '/stop'):
                db_manager.update_log_in(conn, id, 'false')
                db_manager.update_tried_to_log(conn, id, 'false')
                bot.send_message(message.chat.id,
                                 'Вы вышли из учетной записи. Для повторного входа отправьте любое сообщение.')
            else:
                bot.send_message(message.chat.id,
                                 'Нельзя выйти из учетной записи до завершения процесса рассылки. Для остановки рассылки напишите /stop')
        elif (message.text == '/target'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            Hanky_btn = types.KeyboardButton("TARGET FOR HANKY")
            Facial_btn = types.KeyboardButton("TARGET FOR FACIAL")
            markup.add(Hanky_btn, Facial_btn)
            bot.send_message(message.chat.id,
                             'Выберите, цель для какой линии Вы хотите установить',
                             reply_markup=markup)
        elif (message.text =="TARGET FOR HANKY" or message.text == "TARGET FOR FACIAL"):
            bot.send_message(message.chat.id,
                             'Введите цель по показателям в этом месяце. Отправьте каждую цель отдельным сообщением в следующем порядке: ME, NUMBERUNPLANNEDSTOP, Waste.\nВ качестве разделителя дробной части используйте точку.')
            db_manager.update_changing_target(conn, "ME", id, message.text[11:])
        elif (search_res[8] != "NO"):

            if (message.text.isnumeric()):
                if (search_res[8] == "ME"):
                    bot.send_message(message.chat.id, f'Цель по ME для {search_res[9]} введена. Введите цель по NumberOfUnplannedStops.')
                    db_manager.change_target(conn, "ME", float(message.text), search_res[9])
                    db_manager.update_changing_target(conn, "NUS", id, search_res[9])

                if (search_res[8] == "NUS"):
                    bot.send_message(message.chat.id, f'Цель по NumberOfUnplannedStops для {search_res[9]} введена. Введите цель по браку(Waste).')
                    db_manager.change_target(conn, "NUS", float(message.text), search_res[9])
                    db_manager.update_changing_target(conn, "WASTE", id, search_res[9])

                if (search_res[8] == "WASTE"):
                    bot.send_message(message.chat.id, f'Цель по браку (Waste) для {search_res[9]} введена.')
                    db_manager.change_target(conn, "WASTE", float(message.text), search_res[9])
                    db_manager.update_changing_target(conn, "NO", id, "NO")
                    bot.send_message(message.chat.id, db_manager.targets_to_str(db_manager.get_tagrets(conn, line))+'\nЕсли вы допустили ошибку при вводе, просто наберите команду /target снова. При этом Вам придется ввести все цели заново.')

            else:
                bot.send_message(message.chat.id, "Пожалуйста, введите число")

        else:
            bot.send_message(message.from_user.id, 'Неизвестная команда. Напишите /help')
    else:
        if (db_manager.is_tried_to_log(conn, id) == 0):
            bot.send_message(message.chat.id,
                             'Введите пароль. В целях Вашей же безопасности сообщения с вводами пароля будут удалены.')
            db_manager.update_tried_to_log(conn, id, 'true')
        elif (message.text == password):
            db_manager.update_log_in(conn, id, 'true')
            bot.send_message(message.chat.id,
                             'Пароль успешно введен.\nДля запуска напишите /start\nДля остановки напишите /stop\nДля выхода из учетной записи напишите /logout')
            bot.delete_message(message.chat.id, message.message_id)
        else:
            bot.send_message(message.chat.id, 'Неверный пароль, попробуйте еще раз')
            bot.delete_message(message.chat.id, message.message_id)

def brigadier(message):
    id = int(message.chat.id)
    search_res = db_manager.search_user(conn, id)
    if (search_res == 0):
        db_manager.add_active_user(conn, id, 'null', 0, '/stop')
    if (db_manager.is_logged(conn, id)):
        if (message.text == '/start'):
            if (search_res == 0 or search_res[3] == '/stop'):
                bot.send_message(message.chat.id,
                                 'Вы подписались на рассылку сообщений о результатах работы смены. Теперь вам будут приходить результаты работы выбранной линии в конце каждой рабочей смены. Чтобы отписаться, нажмите /stop.')

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                Hanky_btn = types.KeyboardButton("HANKY")
                Facial_btn = types.KeyboardButton("FACIAL")
                Both_btn = types.KeyboardButton("Обе линии")
                markup.add(Hanky_btn, Facial_btn, Both_btn)
                bot.send_message(message.chat.id, 'Выберите линию.', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Вы уже подписаны на расслыку.')

        elif (message.text == '/stop'):
            if (search_res == 0 or search_res[3] == '/stop'):
                bot.send_message(message.chat.id,
                                 'Вы ни на что не подписаны. Чтобы подписаться на информационную рассылку, нажмите /start.')
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                Hanky_btn = types.KeyboardButton("HANKY")
                Facial_btn = types.KeyboardButton("FACIAL")
                Both_btn = types.KeyboardButton("Обе линии")
                markup.add(Hanky_btn, Facial_btn, Both_btn)
                bot.send_message(message.chat.id,
                                 'Вы отписались от рассылки. Чтобы подписаться снова, нажмите /start или сразу выберете линию',
                                 reply_markup=markup)
                db_manager.update_status(conn, id, search_res[1], search_res[2], '/stop')
                stop_process(id)


        elif (message.text == '/help'):
            bot.send_message(message.chat.id,
                             'Для запуска напишите /start\nДля остановки напишите /stop\nДля выхода из учетной записи напишите /logout')

        elif (
                message.text == 'HANKY' or message.text == 'FACIAL' or message.text == 'Обе линии' or message.text == 'жопа'):
            if (search_res == 0 or search_res[3] == '/stop'):
                line = message.text
                if (message.text == 'HANKY' or message.text == 'FACIAL'):
                    bot.send_message(message.chat.id, f"Вы выбрали линию {line}.")
                    start_process(id, line)
                elif (message.text == 'Обе линии'):
                    bot.send_message(message.chat.id, f"Вы выбрали обе линии.")
                    start_process(id, line)
            else:
                bot.send_message(message.chat.id, 'Вы уже подписаны на рассылку.')

        elif (message.text == '/logout'):

            if (search_res == 0 or search_res[3] == '/stop'):
                db_manager.update_log_in(conn, id, 'false')
                db_manager.update_tried_to_log(conn, id, 'false')
                bot.send_message(message.chat.id,
                                 'Вы вышли из учетной записи. Для повторного входа отправьте любое сообщение.')
            else:
                bot.send_message(message.chat.id,
                                 'Нельзя выйти из учетной записи до завершения процесса рассылки. Для остановки рассылки напишите /stop')

        elif (message.text == '/comment'):
            bot.send_message(message.chat.id, 'Отправьте комментарий, начиная со слова "комментарий", например: "комментарий: бла-бла-бла"')
        elif(message.text[0:11] == 'комментарий'):
            pass
            #message.text



        else:
            bot.send_message(message.from_user.id, 'Неизвестная команда. Напишите /help')
    else:
        if (db_manager.is_tried_to_log(conn, id) == 0):
            bot.send_message(message.chat.id,
                             'Введите пароль. В целях Вашей же безопасности сообщения с вводами пароля будут удалены.')
            db_manager.update_tried_to_log(conn, id, 'true')
        elif (message.text == password):
            db_manager.update_log_in(conn, id, 'true')
            bot.send_message(message.chat.id,
                             'Пароль успешно введен.\nДля запуска напишите /start\nДля остановки напишите /stop\nДля выхода из учетной записи напишите /logout')
            bot.delete_message(message.chat.id, message.message_id)
        else:
            bot.send_message(message.chat.id, 'Неверный пароль, попробуйте еще раз')
            bot.delete_message(message.chat.id, message.message_id)



