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
    enable_cache = 'cache_back.cache_from_list()'
    final_query = head_before + '\n' + codebase + '\n' + enable_cache + '\n' + head_after
    if is_query:
        final_query = final_query.replace("'", "''")
    return final_query

def generate_query(notebook, function_name, is_query=False):
    return add_headers(get_code_from_notebook(notebook), function_name, is_query)

def comment_line_by_var_usage(var_name, codebase):
    loc = codebase.split('\n')
    updated_code = ''
    for line in loc:
        temp_line = line.replace(" ", "")
        if temp_line.startswith(var_name):
            line = '#' + line
        updated_code = updated_code + line + '\n'
    return updated_code 

def get_notebook_name(notebook_path):
    return notebook_path.split('.ipynb')[0]