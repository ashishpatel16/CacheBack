import argparse
import cache_back
import headers 

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    notebook_path = params.notebook

    file_name = headers.get_notebook_name(notebook_path)
<<<<<<< HEAD
    cache_back.init_session(db_name=db, db_user=user, db_pass=password, db_host=host, db_port=port, notebook_name=file_name)
    cache_back.send_blob(notebook_path, file_name)
=======
    cache_back.init_session(file_name, db, user, password, host, port)
    cache_back.send_blob(1, notebook_path, file_name)
    # also run the notebook and cache the tables!
    cache_back.execute_as_plpython(notebook_path, file_name)
>>>>>>> main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CacheBack is a tool to cache preprocessing steps for faster analytics.')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--notebook', required=True, help='Notebook path to be pushed on to postgres')

    args = parser.parse_args()

    main(args)