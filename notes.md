* Dataset 
Kaggle : https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews?select=books_data.csv


Running a postgres docker image
sudo docker run -it \
                -e POSTGRES_USER="admin" \
                -e POSTGRES_PASSWORD="root" \
                -e POSTGRES_DB="reviews" \
                -v "$(pwd)/reviews_data:/var/lib/postgresql/data" \
                --network=reviews-network \
                --name reviews-pg-db-new \
                -p 5432:5432 \
                postgres:15.1

Running pgcli 
sudo pgcli -h localhost -p 5432 -u admin -d reviews


Building docker image
sudo docker build -t imageName:tag .

Running the image
sudo docker run -it imageName:tag
sudo docker run -it --network=reviews-network -name reviews-pipeline ingestion:v0.01

Running a pgadmin4 docker image
sudo docker run -it \
                    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
                    -e PGADMIN_DEFAULT_PASSWORD="root" \
                    -p 8080:80 \
                    --network=reviews-network \
                    --name reviews-pgadmin \
                    dpage/pgadmin4

Connect to HPI VPN
snx -s vpn.hpi.de -u ashish.patel

SSH into docker remote container
ssh -p 3700 ashish.patel@172.20.18.12

List running containers
sudo docker ps

Open Bash inside docker container
sudo docker exec -it containerID bash

PEP8 Style Guide 
https://peps.python.org/pep-0008/#documentation-strings


Running cli script
sudo docker run -it --network=reviews-network --name=reviews-cli cli:v01

Execute 
python3 cli.py --user=admin --password=root --db=reviews --port=5432 --host=reviews-pg-db-new-cb

python3 cli.py --user admin --password root --db reviews --port 5432 --host postgres-database --notebook script.ipynb
