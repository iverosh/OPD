from pickle import FALSE, TRUE
import numpy
from datetime import date
import telebot
import schedule
import time
from multiprocessing import *
from telebot import types
import db_manager

# from flask import Flask, request

token = '1638439555:AAH79VtiGN2LuJ_ukB82Gk39JyNechOt_EE'
bot = telebot.TeleBot(token)
# app = Flask(__name__)
APP_NAME = 'secondtestbotautomati'

conn = db_manager.con_to_db()

p: Process
process_list = []

def start_schedule(id, line, process_id):
    job1 = schedule.every().day.at("11:02").do(lambda: send_message2(id)).tag('daily', '1')
    job2 = schedule.every(5).seconds.do(lambda: send_message2(id)).tag('secondly', '2')
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
    global permission
    if (permission):
        process_list.append(p)
        p.start()


def stop_process(id):
    global process_list
    res = db_manager.search_user(conn, id)
    proc_id = res[2]
    p1 = process_list[proc_id]
    p1.terminate()
    process_list.pop(proc_id)


def send_message1(id):
    search_res = db_manager.search_user(conn, id)
    line = search_res[1]
    bot.send_message(id, f'Отправка сообщения по времени. Ваша линия - {line}')



def send_message2(id):
    search_res = db_manager.search_user(conn, id)
    line = search_res[1]
    info_res = db_manager.select_efficiency(conn, line)
    if (info_res == 0):
        bot.send_message(id, f'Данные о показателях эффективности на данной линии отсутствуют')
        db_manager.update_status(conn, id, search_res[1], search_res[2], '/stop')
        stop_process(id)
        global permission
        permission = False
    else:
        if (len(info_res) > 1):
            line = "HANKY"
        for i in info_res:
            assessment = []
            for j in range(3):
                assessment.append('🟢')
            me = i[0]
            nus = i[1]              #достать это все из базы
            waste = i[2]
            efficiency = efficiency_check(conn, line, me, nus, waste)
            if (efficiency[0] == 0):
                print("sas")
                for j in range(3):
                    if(efficiency[j+ 1] == 0):
                        assessment[j] = '🔴'

                brigadiers_id = db_manager.get_brigadiers_id(conn, line)
                bot.send_message(brigadiers_id,f'Линия: {line}\nME: {me} {assessment[0]}\nNUS: {nus} {assessment[1]}\nБрак: {waste} {assessment[2]}')
                bot.send_message(brigadiers_id, "Дайте, пожалуйста комментарий")
                db_manager.update_comment(conn, line, "YES")
                comment = db_manager.get_comment(conn, line)
                while(comment == "YES"):
                    comment = db_manager.get_comment(conn, line)
                    if (comment != "YES"):
                        if (len(comment) < 10):
                            bot.send_message(brigadiers_id, "Ваш комментарий слишком короткий, напишиите, пожалуйста, более подробно")
                            comment = "YES"
                            db_manager.update_comment(conn, line, "YES")
                if (db_manager.search_user(conn, id)[6] != "BRIGADIER"):
                    bot.send_message(id,f'Линия: {line}\nME: {me} {assessment[0]}\nNUS: {nus} {assessment[1]}\nБрак: {waste} {assessment[2]}')
                    bot.send_message(id, "Комментарий от бригадира:\n" + comment)

                line = "FACIAL"
                bot.send_message(brigadiers_id, "Комментарий принят")
                db_manager.update_comment(conn, line, "NO")



def efficiency_check(conn, line, me, nus, waste):

   # return 0

    targets = db_manager.get_targets(conn, line)
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
    query = f"""DELETE * FROM users WHERE PROFILE_TYPE = '{profile_type}'"""
    cursor.execute(query)
    conn.commit()

#print(efficiency_check(conn, "HANKY", 1000, 100, 10))
