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
# default caching
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
                cache_back.cache_outputs[i] = f"SELECT * FROM {df_table}"
else:
    cache_back.cache_from_list()
return cache_back.cache_outputs
'''
    final_query = head_before + '\n' + codebase + '\n' + enable_cache + '\n' + head_after
    if is_query:
        final_query = final_query.replace("'", "''")
    return final_query

def generate_query(notebook, function_name, is_query=False):
    return add_headers(get_code_from_notebook(notebook), function_name, is_query)

def comment_line_by_var_usage(var_name, sql_query, codebase):
    '''
    This needs to comment out all the variable initialisations and in-place methods
    BEFORE caching of that variable occurs and NOT AFTER.
    '''
    is_default_caching = not "add_to_cache" in codebase
    loc = codebase.split('\n')
    updated_code = ''
    not_yet_observed = True # add_to_cache not yet observed?
    for line in loc:
        temp_line = line.replace(" ", "")
        spaces = len(line) - len(line.lstrip()) # number of spaces in front of codes (for proper indentation)
        # rewritten notebook should need not cacheback library, so comment out
        # need to rethink later whether this is actually necessary
        if "from cacheback" in temp_line:
            line = spaces * ' ' + '# ' + line
        # so is init session
        if "cache_back.init_session(" in temp_line:
            line = spaces * ' ' + '# ' + line
        if is_default_caching:
            if temp_line.startswith(var_name+'=') or temp_line.startswith(var_name+'.'):
                line = spaces * ' ' + '# ' + line
                line = _code_for_accessing_cache(line, var_name, sql_query)
        else:
            if not_yet_observed:
                if temp_line.startswith(var_name+'=') or temp_line.startswith(var_name+'.'):
                    line = spaces * ' ' + '# ' + line
                if f"add_to_cache(\'{var_name}\'" in temp_line or f'add_to_cache(\"{var_name}\"' in temp_line:
                    line = spaces * ' ' + '# ' + line
                    line = _code_for_accessing_cache(line, var_name, sql_query)

                    not_yet_observed = False
        updated_code = updated_code + line + '\n'
    return updated_code 

def get_notebook_name(notebook_path):
    return notebook_path.split('.ipynb')[0]


def _code_for_accessing_cache(line, var, sql):
    spaces = len(line) - len(line.lstrip())
    line = line + "\n" + \
        spaces * ' ' + f"cacheback_cur.execute('{sql}')\n" + \
        spaces * ' ' + f"{var} = pd.DataFrame(cacheback_cur.fetchall(), columns = [desc[0] for desc in cacheback_cur.description])\n"
    return line
