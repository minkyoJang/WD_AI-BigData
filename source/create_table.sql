CREATE TABLE url(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    netloc_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    param TEXT,
    bj_id INTEGER NOT NULL,
    title TEXT NOT NULL
    );

CREATE TABLE netloc(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    netloc TEXT NOT NULL
    );

CREATE TABLE chat(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    content TEXT NOT NULL,
    writer_id INTEGER NOT NULL,
    w_time TEXT NOT NULL, 
    url_id INTEGER NOT NULL
    );

CREATE TABLE jamak(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    content TEXT NOT NULL,
    j_time TEXT NOT NULL,
    url_id INTEGER NOT NULL
    );

CREATE TABLE bj(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    netloc_id INTEGER NOT NULL,
    blacklist BOOLEAN NOT NULL DEFAULT FALSE
    );

CREATE TABLE writer(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL
    );