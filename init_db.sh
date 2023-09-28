#!/bin/bash

do_install_postgres=false
do_reset_database=false
do_create_user=false

function install_postgres {
    echo "install postgresgl using sudo"
    sudo apt update && sudo apt install postgresql
}

function start_postgres {
    sudo /etc/init.d/postgresql start
}

function reset_database {
    echo "resetting database"
    sudo -u postgres psql -c "DROP DATABASE IF EXISTS fibers_db"
}

function create_database {
    sudo -u postgres psql -c "CREATE DATABASE fibers_db"
}

function create_schema {
    sudo -u postgres psql -d fibers_db -f ./schema.sql
}

function create_user {
    echo "creating user 'fibers_client'"
    sudo -u postgres psql -c "CREATE USER fibers_client WITH ENCRYPTED PASSWORD 'fiberouspw'"
    sudo -u postgres psql -c "CREATE ROLE database_client"
    sudo -u postgres psql -c "GRANT database_client to fibers_client"
    sudo -u postgres psql -c "GRANT CONNECT ON DATABASE fibers_db TO database_client"
    sudo -u postgres psql -d fibers_db -c "GRANT USAGE ON SCHEMA public TO database_client"
    sudo -u postgres psql -d fibers_db -c "GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO database_client"
    sudo -u postgres psql -d fibers_db -c "GRANT SELECT, INSERT, UPDATE, DELETE ON messages TO database_client"
    sudo -u postgres psql -d fibers_db -c "GRANT SELECT, INSERT, UPDATE, DELETE ON users TO database_client"
}

while getopts "iru" option; do
    case $option in
        i)  do_install_postgres=true ;;
        r)  do_reset_database=true ;;
        u)  do_create_user=true ;;
        *)
            echo "Syntax: $0 [-i|r|u]"
            echo "options:"
            echo "i     Install postgres as superuser"
            echo "r     Reset database (empty every table)"
            echo "u     Create user 'fibers_client'"
            exit 1
            ;;
    esac
done

"$do_install_postgres"  && install_postgres
start_postgres
"$do_reset_database"    && reset_database
create_database
create_schema
"$do_create_user"       && create_user
