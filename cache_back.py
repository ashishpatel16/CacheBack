import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import headers

DB_NAME = ""
DB_USER = ""
DB_PASS = ""
DB_HOST = ""
DB_PORT = 5432 # default
_cached_objects = {}

def init_session(db_name, db_user, db_pass, db_host, db_port=5432):
    """ Initialises Database parameters for connection to postgres """
    global DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT 
    DB_NAME = db_name
    DB_USER = db_user
    DB_PASS = db_pass
    DB_HOST = db_host
    DB_PORT = db_port

def _connect():
    """ Connect to postgres and retrieve all cached variables back into the script """
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    # Retrieve cached data


def insert(df, source_db_table, destination_db_table):
    """ Inserts a given dataframe into postgres """
    try:
        conn_string = f"postgresql://{DB_NAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{source_db_table}"
        db = create_engine(conn_string)
        conn = db.connect()
        df.to_sql(destination_db_table, con=conn, if_exists='replace', index=False)
        print(f"Cached Dataframe successfully to table: {destination_db_table}")
    except Exception as e:
        print(e.args)

def _execute_as_plpython(notebook_path, function_name):
    """ Takes a jupyter notebook and runs it as a plpython function on Postgres Server """
    try:
        plpython_query = headers.generate_query(notebook_path, function_name)
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)

        cur = conn.cursor()
        cur.execute(plpython_query)

        cur.execute(f"SELECT {function_name}();")
        res = cur.fetchall()
        print(res)
    except Exception as e:
        print(e.args)

def add_to_cache(object, name):
    _cached_objects[name] =  object
    print(f"Object added to cache. Current Cache: {_cached_objects.keys()}")

def view_cache():
    print(_cached_objects)

def remove_from_cache(object_name):
    if object_name in _cached_objects.keys():
        del _cached_objects[object_name]
        print(f"Removed {object_name}")
    else:
        raise Exception(f"{object_name} not found.")

remove_from_cache('l')