import psycopg2


# DATABASE_URL = os.environ['postgres://awbxrlmjmiagqj:f285df242c36893c143ec6ccfb7615872d5552e35279703c9a3b267c69584d42@ec2-18-215-96-22.compute-1.amazonaws.com:5432/d5815iauk38hnk']
db_name = "d5815iauk38hnk"


def con_to_db():
    connection = psycopg2.connect(user="awbxrlmjmiagqj",
                                      # пароль, который указали при установке PostgreSQL
                                      password="f285df242c36893c143ec6ccfb7615872d5552e35279703c9a3b267c69584d42",
                                      host="ec2-18-215-96-22.compute-1.amazonaws.com",
                                      port="5432",
                                      database=db_name)
    return connection



def create_table_users(connection):
    cursor = connection.cursor()
    check_query = f"SELECT * FROM pg_catalog.pg_tables WHERE tablename = 'users';"
    cursor.execute(check_query)
    connection.commit()
    res = cursor.fetchall()
    if (len(res) == 0):
        create_table_query = """CREATE TABLE users
                                (
                                    ID integer PRIMARY KEY,
                                    LINE varchar,
                                    PROCESS_ID integer,
                                    LAST_COMMAND varchar,
                                    LOG_IN boolean DEFAULT FALSE,
                                    TRIED_TO_LOG boolean DEFAULT FALSE,
                                    PROFILE_TYPE varchar,
                                    CHANGING_PASS varchar DEFAULT 'NO',
                                    CHANGING_TARGET varchar DEFAULT 'NO',
                                    CHANGING_LINE varchar DEFAULT 'NO'
                                );"""
        cursor.execute(create_table_query)
        connection.commit()
    else:
        check_query = f"SELECT * FROM users"
        cursor.execute(check_query)
        connection.commit()
        res = cursor.fetchall()
    cursor.close()


def create_table_targets(connection):
    cursor = connection.cursor()
    check_query = f"SELECT * FROM pg_catalog.pg_tables WHERE tablename = 'targets';"
    cursor.execute(check_query)
    connection.commit()
    res = cursor.fetchall()
    if (len(res) == 0):
        create_table_query = """CREATE TABLE targets
                                    (
                                        TARGET_TYPE varchar ,
                                        TARGET float ,
                                        LINE varchar
                                    );"""
        cursor.execute(create_table_query)
        connection.commit()
    else:
        check_query = f"SELECT * FROM targets"
        cursor.execute(check_query)
        connection.commit()
        res = cursor.fetchall()
    cursor.close()



def create_table_passwords(connection):
    cursor = connection.cursor()
    check_query = f"SELECT * FROM pg_catalog.pg_tables WHERE tablename = 'passwords';"
    cursor.execute(check_query)
    connection.commit()
    res = cursor.fetchall()
    if (len(res) == 0):
        create_table_query = """CREATE TABLE passwords
                                (
                                    PROFILE_TYPE varchar ,
                                    PASSWORD varchar 
                                );"""
        cursor.execute(create_table_query)
        connection.commit()
    else:
        check_query = f"SELECT * FROM passwords"
        cursor.execute(check_query)
        connection.commit()
        res = cursor.fetchall()
    cursor.close()



def add_active_user(connection, user_id, line, process_id, last_command):
    cursor = connection.cursor()
    add_user_query = f"INSERT INTO users (ID, LINE, PROCESS_ID, LAST_COMMAND) VALUES ({user_id}, '{line}', {process_id}, '{last_command}')"
    cursor.execute(add_user_query)
    connection.commit()



def delete_user(connection, user_id):
    cursor = connection.cursor()
    del_user_query = f"DELETE FROM users WHERE ID = {user_id}"
    cursor.execute(del_user_query)
    connection.commit()



def search_user(connection, user_id):
    cursor = connection.cursor()
    search_query = f"SELECT * FROM users WHERE ID = {user_id}"
    cursor.execute(search_query)
    connection.commit()
    res = cursor.fetchall()
    if (len(res) != 0):
        return res[0]
    else:
        return 0



def is_logged(connection, user_id):
    cursor = connection.cursor()
    query = f"SELECT LOG_IN FROM users WHERE ID = {user_id}"
    cursor.execute(query)
    connection.commit()
    res = cursor.fetchall()
    return (res[0])[0]



def update_log_in(connection, user_id, status):
    cursor = connection.cursor()
    update_query = f"UPDATE users SET LOG_IN = '{status}' WHERE ID = {user_id}"
    cursor.execute(update_query)
    connection.commit()



def is_tried_to_log(connection, user_id):
    cursor = connection.cursor()
    query = f"SELECT TRIED_TO_LOG FROM users WHERE ID = {user_id}"
    cursor.execute(query)
    connection.commit()
    res = cursor.fetchall()
    return (res[0])[0]



def update_tried_to_log(connection, user_id, status):
    cursor = connection.cursor()
    update_query = f"UPDATE users SET TRIED_TO_LOG = '{status}' WHERE ID = {user_id}"
    cursor.execute(update_query)
    connection.commit()



def clear_table_users(connection):
    cursor = connection.cursor()
    query = f"DELETE FROM users WHERE ID > 1"
    cursor.execute(query)
    connection.commit()



def update_status(connection, user_id, line, process_id, last_command):
    cursor = connection.cursor()
    update_query = f"UPDATE users SET LINE = '{line}', PROCESS_ID = {process_id}, LAST_COMMAND = '{last_command}' WHERE ID = {user_id}"
    cursor.execute(update_query)
    connection.commit()



def add_column_to_users(connection):
    cursor = connection.cursor()
    query = "ALTER TABLE users ADD IS_SIGNED BOOLEAN;"
    cursor.execute(query)
    connection.commit()
    print('added')



def select_efficiency(connection, line):
    cursor = connection.cursor()
    if (line != 'Обе линии'):
        query = f"SELECT * FROM lines WHERE line_desc = '{line}';"
    else:
        query = f"SELECT * FROM lines WHERE line_desc = 'HANKY' OR line_desc = 'FACIAL';"
    cursor.execute(query)
    connection.commit
    res = cursor.fetchall()
    if (len(res) != 0):
        return res
    else:
        return 0



def update_changing_pass(connection, profile, id):
    cursor = connection.cursor()
    query = f"""UPDATE users SET CHANGING_PASS = '{profile}' WHERE ID = '{id}'"""
    cursor.execute(query)
    connection.commit()



def change_pass(connection, profile_type, password):
    cursor = connection.cursor()
    query = f"""UPDATE passwords SET PASSWORD = '{password}' WHERE PROFILE_TYPE = '{profile_type}'"""
    cursor.execute(query)
    connection.commit()


def update_changing_target(connection, target_type, id, line):
    cursor = connection.cursor()
    query = f"""UPDATE users SET CHANGING_TARGET = '{target_type}', CHANGING_LINE = '{line}' WHERE ID = '{id}'"""
    cursor.execute(query)
    connection.commit()

def fill_targets(connection):
    cursor = connection.cursor()
    add_user_query = f"INSERT INTO targets (TARGET_TYPE, TARGET, LINE) VALUES ('ME', -1.0, 'FACIAL'), ('NUS', -1.0, 'FACIAL'), ('WASTE', -1.0, 'FACIAL'), ('ME', -1.0, 'HANKY'), ('NUS', -1.0, 'HANKY'), ('WASTE', -1.0, 'HANKY')"
    cursor.execute(add_user_query)
    connection.commit()


def change_target(connection, target_type, target, line):
    cursor = connection.cursor()
    query = f"""UPDATE targets SET TARGET = {target} WHERE TARGET_TYPE = '{target_type}' AND LINE = '{line}'"""
    cursor.execute(query)
    connection.commit()

def get_tagrets(conn, line):
    cursor = conn.cursor()
    query = f"SELECT TARGET from TARGETS WHERE LINE = '{line}'"
    cursor.execute(query)
    result = cursor.fetchall()
    res = []
    for one in result:
        res.append(one[0])
    return res

def targets_to_str(targets):
    return "ME: " + str(targets[0]) + "\nNumberOfUnplannedStops: " + str(targets[1]) + "\nWaste: " + str(targets[2])

def inserting(sql, val, connection):
    with connection.cursor() as cursor:
        cursor.executemany(sql, val)
        connection.commit()

def execute_query (query, connection):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def execute_read_query(query, connection):
    cursor = connection.cursor()
    result = None

    cursor.execute(query)
    result = cursor.fetchall()
    return result

def fill_passwords(connection):

    sql = "INSERT INTO passwords (profile_type, password) VALUES (%s , %s)"
    val = [("admin", "1"), ("technologist", "2"), ("brigadier", "3")]
    inserting(sql, val, connection)


connection = con_to_db()
#update_changing_target(connection, "ME", )

#create_table_targets(connection)
#fill_targets(connection)
print(targets_to_str(get_tagrets(connection,'HANKY')))
#create_table_passwords(con_to_db())

#change_pass(connection, "admin", "123")

#query = "SELECT * from users"
#print(execute_read_query(query, connection))

#query = """DROP table targets;"""
#execute_query(query, connection)

#query = "SELECT * from passwords"
#print(execute_read_query(query, conn))


#create_table_users(connection)
