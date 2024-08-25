docker pull postgres
docker run --name my-postgres -e POSTGRES_USER="admin" -e POSTGRES_PASSWORD="admin" -e POSTGRES_DB="mydatabase" -v my_pgdata:/var/lib/postgresql/data -p 5438:5432 -d postgres
python dbinit.py