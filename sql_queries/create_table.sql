CREATE TABLE IF NOT EXISTS books (
    id         INTEGER       PRIMARY KEY AUTOINCREMENT
                             NOT NULL,
    title      VARCHAR (50),
    author     VARCHAR (40),
    annotation TEXT,
    url        VARCHAR (150),
    image      BLOB
);
