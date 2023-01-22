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

def add_headers(codebase, function_name, add_code_for_caching = False, is_query=False):
    head_before = f"CREATE OR REPLACE FUNCTION {function_name}() " + '''
    RETURNS TEXT
    AS $$ '''

    code_for_caching = '''
# later replace this with one of the cache_back.py functions
# this code will get all the pandas variables from the running code and cache them into DBMS
# import cacheback2
from sqlalchemy import create_engine
conn_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
db = create_engine(conn_string)
conn = db.connect()
for i in dir():
    if not i.startswith('__'):
        if type(eval(i)) == pd.DataFrame:
            eval(i).to_sql(i, con=conn, if_exists='replace', index=False)
            print(i, "is being inserted")
    '''

    head_after = '''$$ LANGUAGE plpython3u;
    '''
    final_query = ''
    if add_code_for_caching: final_query = head_before + '\n' + codebase + '\n' + code_for_caching + '\n' + head_after
    else: final_query = head_before + '\n' + codebase + '\n' + head_after

    if is_query: 
        final_query = final_query.replace("'", "''")
    return final_query

def generate_query(notebook, function_name, add_code_for_caching = False):
    return add_headers(get_code_from_notebook(notebook), function_name, add_code_for_caching)

def comment_line_by_var_usage(var_name, codebase):
    '''
    This needs to comment out all the variable initialisations and in-place methods
    BEFORE caching of that variable occurs and NOT AFTER.
    '''
    loc = codebase.split('\n')
    updated_code = ''
    for line in loc:
        temp_line = line.replace(" ", "")
        if temp_line.startswith(var_name+'=') or temp_line.startswith(var_name+'.'):
            line = '# ' + line
        updated_code = updated_code + line + '\n'
    return updated_code 

def get_notebook_name(notebook_path):
    return notebook_path.split('.ipynb')[0]
