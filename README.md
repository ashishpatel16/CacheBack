# CacheBack

## Setting up the environment and running docker containers 

1. Download reference dataset (books_data.csv) : [Here](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews?select=books_data.csv)
2. Extract and unzip at `ingestion-docker/data/` directory.
3. Build and run containers 
 ```bash 
 docker compose up
 ```
- To stop containers 
```bash
docker compose down
```

- To rebuild containers from source
```bash
docker compose up -d --no-deps --build
```


## Using cli.py to push notebook.ipynb to postgres server
- Build a container as defined by dockerfile in the base directory. Make sure you run the container inside the same network as postgres database.
```bash 
docker build -t image:tag .
```
```bash
docker run -it --network=network image:tag
```

- Using cli.py
```bash
python3 cli.py --user admin --password root --db reviews --port 5432 --host postgres-database
```
