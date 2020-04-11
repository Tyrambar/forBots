import datetime
from random import choice

import psycopg2

from all_queries import *



def random_passw():
    new_passw = ''.join([choice('0123456789') for _ in range(10)])
    check_passw = {exist_p[0] for exist_p in \
            execute_query(conn, ALL_PASSW).fetchall()}
    if new_passw in check_passw:
        random_passw()
    else:
        return new_passw


def create_connection(db_name, db_user, db_password, db_host, db_port=5432):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query, adding_data=None):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        if adding_data:
            cursor.execute(query, adding_data)
        else:
            cursor.execute(query)
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return cursor


def create_add_event_q(args_4_create_arg, host):
    add_event_q = []
    for attr in DEFAULT_ATTRS_EVENT[:-1]:
        add_event_q.append(args_4_create_arg[attr])
    add_event_q.append(host)
    return add_event_q