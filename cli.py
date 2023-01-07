import argparse
import cache_back

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    cache_back.init_session(db, user, password, host, port)
    cache_back.send_blob(1, 'script.ipynb', 'init_nb')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CacheBack is a tool to cache preprocessing steps for faster analytics.')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')

    args = parser.parse_args()

    main(args)