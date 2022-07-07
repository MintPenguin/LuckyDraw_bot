import psycopg2

# for saving file

#create table lucky_draw_file_table
#	(FILE_NAME VARCHAR(255),
#	FILE_CONT TEXT);
#alter table lucky_draw_file_table
#   add constraint pk primary key(file_name);

# file_name: 파일 이름
# file_cont: 파일 내용

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")

DB_TABLE = 'lucky_draw_file_table' # table name in database

def DBselect(file_name):

    sql = 'select file_cont from {0} where file_name = \'{1}\';'.format(DB_TABLE, file_name)
    ret = None

    with psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            ret = cur.fetchone()
            if ret == None: ret == ''
            else: ret = ret[0]

    print('DBselect({0}):'.format(sql), ret)

    return ret

def DBupdate(file_name, file_cont):
    sql = 'insert into {0} values (\'{1}\', \'{2}\') '.format(DB_TABLE, file_name, file_cont)
    sql += 'on conflict on constraint pk '
    sql += 'do update set file_cont = \'{0}\';'.format(file_cont)

    with psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

    print('DBupdate:', sql)