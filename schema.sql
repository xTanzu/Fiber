CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
CREATE TABLE messages (id SERIAL PRIMARY KEY, time TIMESTAMP, author TEXT, content TEXT);

