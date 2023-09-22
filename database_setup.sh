#!/bin/bash
sudo apt update && sudo apt install postgresql
sudo /etc/init.d/postgresql start
sudo -u postgres createdb fibers_db
sudo -u postgres psql -c "CREATE USER fibers_client"
sudo -u postgres psql -c "ALTER USER fibers_client WITH ENCRYPTED PASSWORD 'fiberouspw'"
sudo -u postgres psql -c "CREATE ROLE database_client"
sudo -u postgres psql -c "GRANT database_client to fibers_client"
sudo -u postgres psql -c "GRANT CONNECT ON DATABASE fibers_db TO database_client"
sudo -u postgres psql -d fibers_db -c "GRANT USAGE ON SCHEMA public TO database_client"
sudo -u postgres psql -d fibers_db -c "CREATE TABLE message (id SERIAL PRIMARY KEY, time TEXT, author TEXT, content TEXT)"
sudo -u postgres psql -d fibers_db -c "GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO database_client"
sudo -u postgres psql -d fibers_db -c "GRANT SELECT, INSERT, UPDATE, DELETE ON message TO database_client"





