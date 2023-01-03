import pandas as pd 
from sqlalchemy import create_engine
import time

st = time.time()
df = pd.read_csv('./data/books_data.csv')

conn_string = "postgresql://admin:root@reviews-pg-db:5432/reviews"

engine = create_engine(conn_string)

df.to_sql(name="reviews_data", con=engine, if_exists="replace")
print(df.head(10))

print(f"Executed in {time.time() - st}s")