import mysql.connector
import datetime
import Creds

mydb = mysql.connector.connect(
    host=Creds.host,
    user=Creds.user,
    password=Creds.password,
    database=Creds.database
)
my_cursor = mydb.cursor()

# note current size requirements = 4 for id and 5 bytes per row


def insert_data_for_day(data):
    formula = "INSERT INTO HAL (id, x, y, z) VALUES (%s, %s, %s, %s)"
    my_cursor.executemany(formula, data)
    mydb.commit()


def get_data(table, dt1, dt2):
    id1, id2 = get_id_from_date_range(table, dt1, dt2)
    my_cursor.execute(f"SELECT x, y, z FROM {table} WHERE id BETWEEN {id1} and {id2} ORDER BY id ASC")
    return my_cursor.fetchall()


def get_max(db):
    my_cursor.execute(f"SELECT id from {db} ORDER BY id DESC LIMIT 1")
    max_index = my_cursor.fetchone()[0]
    start_dt = get_ref_start_dt(db)
    max_dt = start_dt + datetime.timedelta(seconds=(max_index/10))
    return max_dt


def get_id_from_date_range(db, date1, date2):
    start_dt = get_ref_start_dt(db)
    end_dt = get_max(db)

    if start_dt <= date1 < date2 <= end_dt:
        time_diff1 = (date1 - start_dt).total_seconds()
        id1 = int(time_diff1 * 10 + 1)
        time_diff2 = (date2 - start_dt).total_seconds()
        id2 = int(time_diff2 * 10)
        return id1, id2
    else:
        print("Invalid datetime range given")


def get_ref_start_dt(db):
    my_cursor.execute(f"SELECT start_datetime FROM reference WHERE db = '{db}'")
    return my_cursor.fetchone()[0]