# prototype

'''
We want to let postgres know which data to be cached.
Maybe: '#annotator'? as a comment form?
'''

# for now, let's just create a simple function 
# that will accept as many variables as possible

import pandas as pd 
from sqlalchemy import create_engine

conn_string = "postgresql://admin:root@reviews-pg-db:5432/reviews"

engine = create_engine(conn_string)

def annotator(*vars):
    for i in vars: # assuming each variable are pandas objects, (for now),
        i.to_sql(name = 'SOMETHING', conn = engine, if_exists="replace")

        # but now we need to think about how to properly save this cached data and retrieve them back


# usage: annotator(df1, df2, df3, df4, ....)
# df1, df2, ... will be cached in DBMS