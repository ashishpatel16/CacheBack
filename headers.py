import json

def get_code_from_notebook(filename, is_query=False):
    f = open(filename, "r")
    data = json.loads(f.read())
    code = ''
    for cell in data['cells']:
        for line in cell['source']:   
            code = code + line
        code = code + '\n'
    return code


def add_headers(codebase, function_name, is_query=False):
    head_before = f"CREATE OR REPLACE FUNCTION {function_name}() " + '''
    RETURNS TEXT
    AS $$ '''
    head_after = '''$$ LANGUAGE plpython3u;
    '''
    enable_cache = '''
if not cache_back.cached_objects:
    from sqlalchemy import create_engine
    conn_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    db = create_engine(conn_string)
    conn = db.connect()
    for i in dir():
        if not i.startswith('__'):
            if type(eval(i)) == pd.DataFrame:
                print(f"inserting {i} ...")
                df_table = cache_back.generate_var_name(i)
                eval(i).to_sql(df_table, con=conn, if_exists='replace', index=False)
                cache_back._cache_outputs[i] = f"SELECT * FROM {df_table}"
else:
    cache_back.cache_from_list(sorted(globals()))
'''
    final_query = head_before + '\n' + codebase + '\n' + enable_cache + '\n' + head_after
    if is_query:
        final_query = final_query.replace("'", "''")
    return final_query

def generate_query(notebook, function_name, is_query=False):
    return add_headers(get_code_from_notebook(notebook), function_name, is_query)

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

