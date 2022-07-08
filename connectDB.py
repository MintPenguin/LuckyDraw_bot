import psycopg2
import os

# for saving file

# file_name: 파일 이름
# file_cont: 파일 내용

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")

DB_TABLE = 'lucky_draw_file_table' # table name in database
DB_FILE_NAME_COL = 'FILE_NAME'
DB_FILE_CONT_COL = 'FILE_CONT'

def DBcreateTable():
    if DB_HOST is None: #if not exists database
        return

    sql = 'create table if not exists {0} '.format(DB_TABLE)
    sql += '({0} VARCHAR(255), '.format(DB_FILE_NAME_COL)
    sql += '{0} TEXT, '.format(DB_FILE_CONT_COL)
    sql += 'constraint pk primary key({0}));'.format(DB_FILE_NAME_COL)

    with psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

    print('create table:', DB_TABLE)

def DBselect(file_name):
    if DB_HOST is None:
        return None

    sql = 'select {0} from {1} where {2} = \'{3}\';'.format(DB_FILE_CONT_COL, DB_TABLE, DB_FILE_NAME_COL, file_name)
    ret = None

    with psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            ret = cur.fetchone()

            print('DBselect({0}):'.format(sql), ret)
            if ret is None:
                ret = ''
                DBupdate(file_name, ret)
            else:
                ret = ret[0]

    return ret

def DBupdate(file_name, file_cont):
    if DB_HOST is None:
        return

    sql = 'insert into {0} values (\'{1}\', \'{2}\') '.format(DB_TABLE, file_name, file_cont)
    sql += 'on conflict on constraint pk '
    sql += 'do update set {0} = \'{1}\';'.format(DB_FILE_CONT_COL, file_cont)

    with psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

    print('DBupdate:', sql)