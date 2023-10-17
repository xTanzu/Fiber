CREATE TABLE users (user_id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
CREATE TABLE fibers (fiber_id SERIAL PRIMARY KEY, owner_id INTEGER REFERENCES users, fibername TEXT UNIQUE, description TEXT);
CREATE TABLE tags (tag_id SERIAL PRIMARY KEY, tag TEXT UNIQUE);
CREATE TABLE messages (message_id SERIAL PRIMARY KEY, time TIMESTAMP, author_id INTEGER REFERENCES users, fiber_id INTEGER REFERENCES fibers,content TEXT);
CREATE TABLE user_fibers (user_id INTEGER REFERENCES users, fiber_id INTEGER REFERENCES fibers, PRIMARY KEY (user_id, fiber_id));
CREATE TABLE fiber_tags (fiber_id INTEGER REFERENCES fibers, tag_id INTEGER REFERENCES tags, PRIMARY KEY (fiber_id, tag_id));

