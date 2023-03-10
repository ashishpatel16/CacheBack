import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import headers
import hashlib
import dependency as dep
import os

DB_NAME = ""
DB_USER = ""
DB_PASS = ""
DB_HOST = ""
DB_PORT = 5432 # default
BLOB_TABLE_NAME = "pipeline_blobs"
NOTEBOOK_NAME = ""
NOTEBOOK_CODE = ""
cached_objects = {}
cache_outputs = {}
CACHE_TABLE_NAME = "cached_tables"


def init_session(db_name, db_user, db_pass, db_host, db_port=5432, notebook_name=''):
    """ Initialises Database parameters for connection to postgres """
    global DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT, NOTEBOOK_CODE, NOTEBOOK_NAME
    DB_NAME = db_name
    DB_USER = db_user
    DB_PASS = db_pass
    DB_HOST = db_host
    DB_PORT = db_port
    NOTEBOOK_NAME = notebook_name
    # currently this is causing problem, so temporarily disabled
    #dep.handle_imports(notebook_name + '.ipynb')
    print(DB_USER,DB_PASS, DB_HOST, DB_PORT)
    print('init session invoked')

def _connect():
    """ Connect to postgres and retrieve all cached variables back into the script """
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    print('_connect invoked')
    return conn


def insert(df, destination_db_table):
    """ Inserts a given dataframe into postgres """
    try:
        conn_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(conn_string)
        db = create_engine(conn_string)
        print('created engine')
        conn = db.connect()
        print('connected')
        df.to_sql(destination_db_table, con=conn, if_exists='replace', index=False, chunksize = 1000)
        print(f"Cached Dataframe successfully to table: {destination_db_table}")
    except Exception as e:
        print(e.args[0])

# When executing code,
# 1. get all lists of pandas dataframes
# 2. insert them into cached table (cached_tables)

# the default behaviour of commit should be every pandas table needs to be cached
def execute_as_plpython(notebook_path, function_name):
    """ Takes a jupyter notebook and runs it as a plpython function on Postgres Server """
    try:
        plpython_query = headers.generate_query(notebook_path,
                                                function_name,
                                                is_query=False)
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)

        print(f"EXECUTING -->\n{plpython_query}")
        cur = conn.cursor()
        cur.execute(plpython_query)

        print('RUNNING SCRIPT')
        cur.execute(f"SELECT {function_name}();")
        res = cur.fetchone()
        print("these variables were cached:")
        # the cursor returns the cache_outputs from plpython instance as "string" format.
        # therefore, some code for properly parsing is needed. :)
        global cache_outputs
        for i in res:
            cache_outputs = eval(i)
        for i in cache_outputs.keys():
            print(i)
        print('Successful execution of plpython')
        conn.commit()
        cur.close()
    except Exception as e:
        print(e.args[0])

def add_to_cache(table: pd.DataFrame, object: str):
    '''
    please make the table varialbe and the object name the same
    i.e., add_to_cache(df1, 'df1')
    '''
    cached_objects[object] =  table
    print(f"Object added to cache. Current Cache: {cached_objects.keys()}")

def view_cache():
    print(cached_objects)

def remove_from_cache(object_name):
    if object_name in cached_objects.keys():
        del cached_objects[object_name]
        print(f"Removed {object_name}")
    else:
        raise Exception(f"{object_name} not found.")

def send_blob(notebook_path, file_name):
    _create_blob_table()
    try:
        conn = _connect()
        cur = conn.cursor()
        file_data = read_notebook_as_binary(notebook_path)
        global NOTEBOOK_CODE 
        NOTEBOOK_CODE = headers.get_code_from_notebook(filename=notebook_path)
        function_name = headers.get_notebook_name(notebook_path) + '_script'

        plpython_script = headers.generate_query(notebook_path, function_name, is_query=True)
        print('generated query')
        print(plpython_script)
        blob = psycopg2.Binary(file_data)
        print('file read as binary')

        query = f"INSERT INTO {BLOB_TABLE_NAME} (file_name, source_notebook, plscript) VALUES('{file_name}',{blob},'''{plpython_script}''')"
        print(query)
        cur.execute(query)
        print('Blob inserted')
        conn.commit()
        cur.close()

        execute_as_plpython(notebook_path, 'execute_plpython')

        print("this is the rewritten pipeline")
        print("-------------------------------")
        
        
    except Exception as e:
        print(e.args[0])

def _create_blob_table():
    try:
        conn = _connect()
        cur = conn.cursor()
        query = f"CREATE TABLE IF NOT EXISTS {BLOB_TABLE_NAME} (id SERIAL PRIMARY KEY, upload_date TIMESTAMP default current_timestamp, file_name TEXT, source_notebook BYTEA, plscript TEXT, updated_notebook BYTEA);"
        print(query)
        cur.execute(query)
        conn.commit() 
        cur.close()
    except Exception as e:
        print(e.args)

def read_notebook_as_binary(notebook_path):
    with open(notebook_path, 'rb') as file:
        data = file.read()
    return data

def cache_from_list():
    try:
        print('Caching Objects ... ')       
        for df_name, df in cached_objects.items():
            print(f"inserting {df_name} ...")
            df_table = generate_var_name(df_name)
            insert(df,destination_db_table=df_table)
            cache_outputs[df_name] = f"SELECT * FROM {df_table}"
        
        # rewrite_pipeline()
    except Exception as e:
        print(e.args[0])

def read_existing_cache(notebook_path: str):
    """
    Attempts to check whether DBMS already has existing cache for current notebook.
    If it does not exist, prints that the cache does not exist.
    """
    print("Attemping to retrieve cache (if existing)")
    try:
        conn = _connect()
        cur = conn.cursor()
        file_data = read_notebook_as_binary(notebook_path)
        blob = psycopg2.Binary(file_data)
        query = f"SELECT * FROM {BLOB_TABLE_NAME} WHERE source_notebook = {blob}"
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        print(res)
        cur.close()

    except Exception as e:
        print(e.args)

def generate_var_name(df_name, filename=NOTEBOOK_NAME):
    hash = hashlib.md5(filename.encode()).hexdigest()
    generated_name = df_name + '_' + hash
    return generated_name

def rewrite_pipeline():
    global NOTEBOOK_CODE
    updated_code = ''
    for df_name, query in cache_outputs.items():
        
        # commenting and also adding newly variable assignments
        updated_code = headers.comment_line_by_var_usage(df_name, query, NOTEBOOK_CODE)
        NOTEBOOK_CODE = updated_code
        #headers.rewrite_var_definition(df_name, query, updated_code)
        
    # handling sql connection code in front of everything
    NOTEBOOK_CODE = get_sql_conn_code() + updated_code
    print('*********************************')
    print(NOTEBOOK_CODE)


def get_sql_conn_code():
    explanation = "# FOLLOWING IMPORT GENERATED BY CACHEBACK"
    import_code = "import psycopg2\nimport pandas as pd"
    l1 = f"cacheback_conn = psycopg2.connect(database='{DB_NAME}', user='{DB_USER}', password='{DB_PASS}', host='{DB_HOST}', port={DB_PORT})"
    l2 = "cacheback_cur = cacheback_conn.cursor()"
    endline = "#------------------------------------------"
    return explanation + '\n' + import_code + '\n' + l1 + '\n' + l2 + '\n' + endline + '\n\n'


def return_new_notebook(nb_name):
    # first save rewritten notebook code as .py
    file = open(f"./{nb_name}_rewritten.py", 'w')
    file.write(NOTEBOOK_CODE)
    file.close()
    # then convert .py to .ipynb using jupytext
    os.system(f'jupytext --to notebook {nb_name}_rewritten.py')
