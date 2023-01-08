import pandas as pd 
from sqlalchemy import create_engine
import time

st = time.time()
df = pd.read_csv('data/Reviews.csv')

# this ip address needs to be replaced with postgres's container IP addr
# to check, docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres-docker
ip_addr = "localhost"
conn_string = f"postgresql://admin:root@{ip_addr}:5432/reviews"

engine = create_engine(conn_string)

df.to_sql(name="reviews_data", con=engine, if_exists="replace")
print(df.head(10))

print(f"Executed in {time.time() - st}s")