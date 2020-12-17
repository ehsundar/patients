DROP TABLE IF EXISTS org;
DROP TABLE IF EXISTS perm;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS perm_linker;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS res;
DROP TABLE IF EXISTS report;

CREATE TABLE org
(
    slug       VARCHAR(32) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    name       VARCHAR(32)
);

CREATE TABLE perm
(
    slug       VARCHAR(32) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    name       VARCHAR(32)
);

CREATE TABLE users
(
    username   VARCHAR(32) PRIMARY KEY,
    created_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,

    password   VARCHAR(64) NOT NULL,

    org        VARCHAR(32),
    FOREIGN KEY (org) REFERENCES org (slug)
);

CREATE TABLE perm_linker
(
    id         SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    username   VARCHAR(32),
    perm       VARCHAR(32),
    FOREIGN KEY (username) REFERENCES users (username),
    FOREIGN KEY (perm) REFERENCES perm (slug)
);

CREATE TABLE patient
(
    id           SERIAL PRIMARY KEY,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    phone        VARCHAR(11),
    name         VARCHAR(32),
    gender       VARCHAR(32),

    creator_user VARCHAR(32),
    FOREIGN KEY (creator_user) REFERENCES users (username)
);

CREATE TABLE res
(
    id         SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE report
(
    id           SERIAL PRIMARY KEY,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    patient      INTEGER,
    creator_user VARCHAR(32),
    FOREIGN KEY (patient) REFERENCES patient (id),
    FOREIGN KEY (creator_user) REFERENCES users (username)
);
