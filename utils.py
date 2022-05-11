from pickle import FALSE, TRUE
import numpy
from datetime import date
import telebot
import schedule
import time
from multiprocessing import *
from telebot import types
import db_manager
from datetime import date

# from flask import Flask, request

token = '5145537162:AAFYmOR1uW8eTwT7sODyeQONBrcT9nQySVw' # 5145537162:AAFYmOR1uW8eTwT7sODyeQONBrcT9nQySVw - Геннадий 5252133698:AAF-w9vgM1tmfNIVNJThzHF77iX0IZZ0Bl4
bot = telebot.TeleBot(token)
# app = Flask(__name__)
APP_NAME = 'secondtestbotautomati'

conn = db_manager.con_to_db()

p: Process
process_list = []

def remind_techlonogist():
    tech_res = db_manager.get_technologists_id(conn)
    today = str(date.today().day)
    print(today)
    if (date.today().day == 12):
        for tech_id in tech_res:
            bot.send_message(tech_id, "Сегодня первое число, введите, пожалуйста, целевые показатели на этот месяц, если вы этого еще не сделали\nИспользуйте команду /target")

def remind_schedule():
    job = schedule.every().day.at("09:00").do(lambda: remind_techlonogist()).tag('remind', '11')
    while (True):  # Запуск цикла
        schedule.run_pending()
        time.sleep(1)

def start_schedule(id, line, process_id):
    job1 = schedule.every().day.at("11:02").do(lambda: send_message2(id)).tag('daily', '1')
    job2 = schedule.every(5).seconds.do(lambda: send_message2(id)).tag('secondly', '2') #15 sek
    res = db_manager.search_user(conn, id)
    if (res == 0):
        db_manager.add_active_user(conn, id, line, process_id, '/start')
    else:
        db_manager.update_status(conn, id, line, process_id, '/start')
    while (True):  # Запуск цикла
        schedule.run_pending()
        time.sleep(1)


permission = True


def start_process(id, line):  # Запуск Process
    global process_list
    global p
    free_proc_id = len(process_list)
    p = Process(target=start_schedule, args=((id, line, free_proc_id)))
    process_list.append(p)
    p.start()


def stop_process(id):
    global process_list
    res = db_manager.search_user(conn, id)
    proc_id = res[2]
    p1 = process_list[proc_id]
    p1.terminate()
    process_list.pop(proc_id)
    db_manager.update_proc_id(conn, proc_id)


def send_message1(id):
    search_res = db_manager.search_user(conn, id)
    line = search_res[1]
    bot.send_message(id, f'Отправка сообщения по времени. Ваша линия - {line}')



def send_message2(id):  # сделать проверку на наличие бригадира
    search_res = db_manager.search_user(conn, id)
    line = search_res[1]
    line_hanky = "HANKY"
    line_facial = "FACIAL"
    db_manager.update_comment(conn, line_hanky, "NO")
    db_manager.update_comment(conn, line_facial, "NO")
    info_res = db_manager.select_efficiency(conn, line)

    if (info_res == 0):
        bot.send_message(id, f'Данные о показателях эффективности на данной линии отсутствуют')
        db_manager.update_status(conn, id, search_res[1], search_res[2], '/stop')
        stop_process(id)
        global permission
        permission = False
    else:
        if (len(info_res) == 1):


            assessment = []
            for j in range(3):
                assessment.append('🟢')
            me = info_res[0][0]
            nus = info_res[0][1]              #достать это все из базы
            waste = info_res[0][2]
            efficiency = efficiency_check(conn, line, me, nus, waste)
            if (efficiency[0] == 0):
                print("sas")
                for j in range(3):
                    if(efficiency[j+ 1] == 0):
                        assessment[j] = '🔴'

                brigadiers_id = db_manager.get_brigadiers_id(conn, line)
                if (brigadiers_id == -1):
                    bot.send_message(id, "Отсутствуют бригадиры на данной линии.")
                    db_manager.update_status(conn, id, search_res[1], search_res[2], '/stop')
                    stop_process(id)
                    return
                bot.send_message(brigadiers_id,f'Линия: {line}\nME: {me} {assessment[0]}\nNUS: {nus} {assessment[1]}\nБрак: {waste} {assessment[2]}')
                bot.send_message(brigadiers_id, "Дайте, пожалуйста комментарий")
                db_manager.update_comment(conn, line, "YES")
                comment = db_manager.get_comment(conn, line)
                while(comment == "YES" or len(comment) < 10):
                    comment = db_manager.get_comment(conn, line)
                    print(comment)

                    if (comment != "YES"):
                        if (len(comment) < 10):
                            print("короткий комент")
                            bot.send_message(brigadiers_id, "Ваш комментарий слишком короткий, напишиите, пожалуйста, более подробно")
                            comment = "YES"
                            db_manager.update_comment(conn, line, "YES")
                if (db_manager.search_user(conn, id)[6] != "BRIGADIER"):
                    bot.send_message(id,f'Линия: {line}\nME: {me} {assessment[0]}\nNUS: {nus} {assessment[1]}\nБрак: {waste} {assessment[2]}')
                    bot.send_message(id, "Комментарий от бригадира:\n" + comment)
                bot.send_message(brigadiers_id, "Комментарий принят")
            else:
                bot.send_message(id,
                                 f'Линия: {line}\nME: {me} {assessment[0]}\nNUS: {nus} {assessment[1]}\nБрак: {waste} {assessment[2]}')

        else:

            assessment_hanky = []
            assessment_facial = []
            for j in range(3):
                assessment_hanky.append('🟢')
            for j in range(3):
                assessment_facial.append('🟢')

            me_hanky = info_res[0][0]
            nus_hanky = info_res[0][1]  # достать это все из базы
            waste_hanky = info_res[0][2]
            efficiency_hanky = efficiency_check(conn, line_hanky, me_hanky, nus_hanky, waste_hanky)

            me_facial = info_res[1][0]
            nus_facial = info_res[1][1]  # достать это все из базы
            waste_facial = info_res[1][2]
            efficiency_facial = efficiency_check(conn, line_facial, me_facial, nus_facial, waste_facial)

            if (efficiency_hanky[0] == 0 or efficiency_facial[0] == 0): #добавить елс

                if (efficiency_hanky[0] == 0):
                    for j in range(3):
                        if (efficiency_hanky[j + 1] == 0):
                            assessment_hanky[j] = '🔴'
                    brigadiers_id_hanky = db_manager.get_brigadiers_id(conn, line_hanky)
                    bot.send_message(brigadiers_id_hanky,
                                     f'Линия: {line_hanky}\nME: {me_hanky} {assessment_hanky[0]}\nNUS: {nus_hanky} {assessment_hanky[1]}\nБрак: {waste_hanky} {assessment_hanky[2]}')
                    bot.send_message(brigadiers_id_hanky, "Дайте, пожалуйста комментарий")
                    db_manager.update_comment(conn, line_hanky, "YES")
                    comment_hanky = db_manager.get_comment(conn, line_hanky)


                if (efficiency_facial[0] == 0):
                    for j in range(3):
                        if (efficiency_facial[j + 1] == 0):
                            assessment_facial[j] = '🔴'
                    brigadiers_id_facial = db_manager.get_brigadiers_id(conn, line_facial)
                    bot.send_message(brigadiers_id_facial,
                                     f'Линия: {line_facial}\nME: {me_hanky} {assessment_hanky[0]}\nNUS: {nus_hanky} {assessment_hanky[1]}\nБрак: {waste_hanky} {assessment_hanky[2]}')
                    bot.send_message(brigadiers_id_facial, "Дайте, пожалуйста комментарий")
                    db_manager.update_comment(conn, line_facial, "YES")
                    comment_facial = db_manager.get_comment(conn, line_hanky)

                while (comment_hanky == "YES" or len(comment_hanky) < 10 or comment_facial == "YES" or len(comment_facial) < 10):
                    comment_hanky = db_manager.get_comment(conn, line_hanky)
                    comment_facial = db_manager.get_comment(conn, line_facial)


                    if (comment_hanky == "YES" or len(comment_hanky) < 10 ):
                        if (comment_hanky != "YES"):
                            if (len(comment_hanky) < 10):
                                print("короткий комент")
                                bot.send_message(brigadiers_id_hanky,
                                                 "Ваш комментарий слишком короткий, напишиите, пожалуйста, более подробно")
                                comment_hanky = "YES"
                                db_manager.update_comment(conn, line_hanky, "YES")
                    if (comment_facial == "YES" or len(comment_facial) < 10 ):
                        if (comment_facial != "YES"):
                            if (len(comment_facial) < 10):
                                print("короткий комент")
                                bot.send_message(brigadiers_id_facial,
                                                 "Ваш комментарий слишком короткий, напишиите, пожалуйста, более подробно")
                                comment_facial = "YES"
                                db_manager.update_comment(conn, line_facial, "YES")
                if (db_manager.search_user(conn, id)[6] != "BRIGADIER"):
                    bot.send_message(id,
                                     f'Линия: {line_hanky}\nME: {me_hanky} {assessment_hanky[0]}\nNUS: {nus_hanky} {assessment_hanky[1]}\nБрак: {waste_hanky} {assessment_hanky[2]}')
                    if (efficiency_facial[0] == 0):
                        bot.send_message(id, "Комментарий от бригадира:\n" + comment_hanky)
                        bot.send_message(brigadiers_id_hanky, "Комментарий принят")

                    bot.send_message(id,
                                     f'Линия: {line_facial}\nME: {me_facial} {assessment_facial[0]}\nNUS: {nus_facial} {assessment_facial[1]}\nБрак: {waste_facial} {assessment_facial[2]}')
                    if (efficiency_facial[0] == 0):
                        bot.send_message(id, "Комментарий от бригадира:\n" + comment_facial)
                        bot.send_message(brigadiers_id_facial, "Комментарий принят")

                    bot.send_message(brigadiers_id_facial, "Комментарий принят")



def efficiency_check(conn, line, me, nus, waste):

    # return [1]

    targets = db_manager.get_targets(conn, line)
    print(targets)
    if targets[0] > me or targets[1] < nus or targets[2] < waste:
        res = [0]
        res.append(0 if targets[0] > me else 1)
        res.append(0 if targets[1] < nus else 1)
        res.append(0 if targets [2] < waste else 1)
        return res
    else:
        return [1]

def logout_after_change_pass(conn, profile_type):
    cursor = conn.cursor()
    query = f"""SELECT ID FROM users WHERE LAST_COMMAND = '/start' AND PROFILE_TYPE = '{profile_type}'"""
    cursor.execute(query)
    ids = cursor.fetchall()
    for id in ids:
        stop_process(id)
    query = f"""DELETE FROM users WHERE PROFILE_TYPE = '{profile_type}'"""
    cursor.execute(query)
    conn.commit()

#logout_after_change_pass(conn, "BRIGADIER")

#print(efficiency_check(conn, "FACIAL", 1000, 100, 10))
