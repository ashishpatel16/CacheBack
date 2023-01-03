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

def add_headers(codebase):
    head_before = '''CREATE FUNCTION my_func()
    AS $$ '''
    head_after = '''$$ LANGUAGE plpythonu;'''
    return head_before + '\n' + codebase + '\n' +head_after

def generate_query(notebook):
    return add_headers(get_code_from_notebook(notebook))

print(add_headers(get_code_from_notebook('script.ipynb')))