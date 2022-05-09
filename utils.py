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

token = '5145537162:AAFYmOR1uW8eTwT7sODyeQONBrcT9nQySVw'
bot = telebot.TeleBot(token)
# app = Flask(__name__)
APP_NAME = 'secondtestbotautomati'
password = '123'
conn = db_manager.con_to_db()


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
        for i in range(numpy.shape(info_res)[0]):
            assessment = '🟢'
            total = info_res[i][2]
            defects = info_res[i][3]
            efficiency = (total - defects) / total * 100
            efficiency_str = format(efficiency, '.2f')
            if (efficiency < 90):
                assessment = '🔴'
            bot.send_message(id,
                             f'Линия: {line}\nВсего произведено: {total}\nБрак: {defects}\nЭффективность: {efficiency_str}{assessment}')

def efficiency_check(conn, line):
    me = 12
    nus = 3
    waste = 7 # тут достаем показатели из бд, а пока что так
    targets = db_manager.get_targets(conn, line)
    if targets[0] < me or targets[1] < nus or targets [2] < waste:
        # достаем из базы user'a с profile_type = 'brigadier' и отправляем ему сообщение, прося ввести комментарий
        pass
