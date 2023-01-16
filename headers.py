import json

def get_code_from_notebook(filename):
    f = open(filename, "r")
    data = json.loads(f.read())
    code = ''
    for cell in data['cells']:
        for line in cell['source']:   
            code = code + line
        code = code + '\n'
    return code

def add_headers(codebase, function_name, add_code_for_caching = False):
    head_before = f"CREATE FUNCTION {function_name}() " + '''
    RETURNS TEXT
    AS $$ '''

    code_for_caching = '''
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
    '''

    head_after = '''$$ LANGUAGE plpython3u;
    '''

    if add_code_for_caching: return head_before + '\n' + codebase + '\n' + \
        code_for_caching + '\n' + head_after
    else: return head_before + '\n' + codebase + '\n' + head_after

def generate_query(notebook, function_name, add_code_for_caching = False):
    return add_headers(get_code_from_notebook(notebook), function_name, add_code_for_caching)
