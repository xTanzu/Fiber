-- CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
-- Muista päivittää myös taulu message monikoksi
CREATE TABLE message (id SERIAL PRIMARY KEY, time TEXT, author TEXT, content TEXT);

