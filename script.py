import psycopg2
import pandas as pd
import time 

DB_NAME = "reviews"
DB_USER = "admin"
DB_PASS = "root"
DB_HOST = "localhost"
DB_PORT = 5432
TABLE_NAME = "reviews_data2"

try:
    start_time = time.time()
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

    print("Database connected successfully")

    fetch_query = f"SELECT * FROM {TABLE_NAME}"
    fetch_columns_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{TABLE_NAME}'"

    
    column_names = []
    cur = conn.cursor()
    cur.execute(fetch_columns_query)

    # Fetch column names from the table for our pandas dataframe
    for s in cur.fetchall():
        column_names.append(s[0])

    print(column_names)

    # Fetch actual data from postgres and instantiate DataFrame
    cur.execute(fetch_query)
    res = cur.fetchall()
    df = pd.DataFrame(res, columns=column_names)
    print(df.head())
    
    write_query = ""
    cur.close()
    conn.close()
    end_time = time.time()
    print(f"***** Completed in {(end_time-start_time)} seconds. Dataframe shape : {df.shape}")


    #print(dir())

    # later replace this with one of the cache_back.py functions
    # this code will get all the pandas variables from the running code and cache them into DBMS
    from sqlalchemy import create_engine
    conn_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    db = create_engine(conn_string)
    conn = db.connect()
    for i in dir():
        if not i.startswith('__'):
            if type(eval(i)) == pd.DataFrame:
                eval(i).to_sql(i, con=conn, if_exists='replace', index=False)

except Exception as e:
    print(f"Error : {e.args}")

'''
Step 1 : Load data from RDBMS into dataframe.
Step 2 : Perform some data manipulations (Adding or droppinng columns or normalising them). Send the .ipynb file on to server.
            2.1. Take the ipynb file, parse json and build the complete code into a single string.
            2.2. Append the headers and footers as per the CREATE FUNCTION construct for plpython.
            2.3. Execute the query generated for plpython, triggered from client machine.
Step 3 : Convert the .ipynb file on server into a .db file using dill. - not now
Step 4 : Save results on a separate table. 
Step 5 : Retrieve results from database
'''