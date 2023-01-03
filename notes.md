* Converting .sqlite to .sql dump file

First run this command to prevent errors which I resolved somehow:

SET CLIENT_ENCODING TO 'utf8';
.open C:\\Users\\ashis\\OneDrive\\Desktop\\IDPP\\CustomNotebook\\dump.sql

* Loading .sql file into postgres using psql cli

\i 'C:\\Users\\ashis\\OneDrive\\Desktop\\IDPP\\CustomNotebook\\dump.sql';

 * Dataset 

 Download at Kaggle : https://www.kaggle.com/datasets/joychakraborty2000/amazon-customers-data?select=database.sqlite
 
 Direct link : https://storage.googleapis.com/kaggle-data-sets/1272761/2121118/compressed/database.sqlite.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20221210%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20221210T215420Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=483811befd7ec6d74912ddc9d60a2fcf6361fffe0248e0e792d00d9ac1c54cfedf79792646693c8449be14113ed86b8cb31f2fe740f1a8fd4319d1eaa64086eb00170c82d4105f4147c917c2b7459973e294bed3e904ccf4b1690ab3ef73d461432c63f61e6289f9cc08e759a897897d66bb5c53bbb8ed489e6c1891e14cdb15a640d20d8ef69ac3a9d9978c2a71a2b95897a16336c169b23a65f9b4acbfa9bc5c7600f650153755cbc06856c074fbcec857026215a143be791b5e5833ef392e33113487ef4450f96f8a36a7e40e0c5ced3945133d0add2564e571716478e006f01a8fe823ed2efbe6693f77fe6cf1c09ecf9bdcb7177d0a4af821252c2c9984


Running a postgres docker image
 docker run -it \
                -e POSTGRES_USER="admin" \
                -e POSTGRES_PASSWORD="root" \
                -e POSTGRES_DB="reviews" \
                -v "$(pwd)/reviews_data:/var/lib/postgresql/data" \
                -p 5432:5432 \
                postgres:15

Running pgcli 
sudo pgcli -h localhost -p 5432 -u admin -d reviews


Building docker image
sudo docker build -t imageName:tag .

Running the image
sudo docker run -it imageName:tag

