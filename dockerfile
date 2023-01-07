FROM python:3.9

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./cache_back.py cache_back.py
COPY ./cli.py cli.py
COPY ./headers.py headers.py
COPY ./script.ipynb script.ipynb 

ENTRYPOINT ["bash"]