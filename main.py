from profiles import *



@bot.message_handler(content_types=['text'])
def start(message):
    brigadier(message)

p: Process
process_list = []
last_command: str = ' '

if (__name__ == '__main__'):
    try:
        db_manager.create_table_users(conn)
        db_manager.create_table_targets(conn)
        db_manager.create_table_passwords(conn)
        bot.polling(none_stop=True)
    except:
        pass
    finally:
        conn.close()