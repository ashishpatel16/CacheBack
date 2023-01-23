FROM python:3.9

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./cache_back.py cache_back.py
COPY ./cli.py cli.py
COPY ./headers.py headers.py
COPY ./script.ipynb script.ipynb 
COPY ./script.py script.py 

# ENTRYPOINT ["python3", "cli.py", "--user=admin", "--password=root", "--db=reviews", "--port=5432", "--host=postgres-database", "--notebook=script.ipyb"]
ENTRYPOINT [ "bash" ]