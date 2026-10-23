CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    fam VARCHAR(100),
    name VARCHAR(100),
    otc VARCHAR(100),
    phone VARCHAR(20)
);

CREATE TABLE coords (
    id SERIAL PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    height INTEGER NOT NULL
);

CREATE TABLE pereval_images (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    data TEXT
);

CREATE TABLE pereval_added (
    id SERIAL PRIMARY KEY,
    beauty_title VARCHAR(255),
    title VARCHAR(255),
    other_titles VARCHAR(255),
    connect TEXT,
    add_time TIMESTAMP,
    user_id INTEGER REFERENCES users(id),
    coord_id INTEGER REFERENCES coords(id),
    level_winter VARCHAR(10),
    level_spring VARCHAR(10),
    level_summer VARCHAR(10),
    level_autumn VARCHAR(10),
    status VARCHAR(20) DEFAULT 'new'
);

CREATE TABLE pereval_images_relation (
    pereval_id INTEGER REFERENCES pereval_added(id),
    image_id INTEGER REFERENCES pereval_images(id),
    PRIMARY KEY (pereval_id, image_id)
);