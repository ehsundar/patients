DROP TABLE IF EXISTS org CASCADE;
CREATE TABLE org
(
    slug       VARCHAR(32) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    name       VARCHAR(32)
);

DROP TABLE IF EXISTS perm CASCADE;
CREATE TABLE perm
(
    slug       VARCHAR(32) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    name       VARCHAR(32)
);

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users
(
    username   VARCHAR(32) PRIMARY KEY,
    created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    password   VARCHAR(256) NOT NULL,

    org        VARCHAR(32),
    FOREIGN KEY (org) REFERENCES org (slug)
);

DROP TABLE IF EXISTS perm_linker CASCADE;
CREATE TABLE perm_linker
(
    id         SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    username   VARCHAR(32),
    perm       VARCHAR(32),
    FOREIGN KEY (username) REFERENCES users (username),
    FOREIGN KEY (perm) REFERENCES perm (slug)
);

DROP TABLE IF EXISTS patient CASCADE;
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

DROP TABLE IF EXISTS res CASCADE;
CREATE TABLE res
(
    id         SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    start_t    TIMESTAMP,
    end_t      TIMESTAMP,
    cap        INTEGER
);

DROP TABLE IF EXISTS state CASCADE;
CREATE TABLE state
(
    slug VARCHAR(32) PRIMARY KEY,
    name VARCHAR(32)
);

DROP TABLE IF EXISTS report CASCADE;
CREATE TABLE report
(
    id           SERIAL PRIMARY KEY,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    patient      INTEGER,
    creator_user VARCHAR(32),
    res          INTEGER,
    state        VARCHAR(32),
    FOREIGN KEY (patient) REFERENCES patient (id),
    FOREIGN KEY (creator_user) REFERENCES users (username),
    FOREIGN KEY (res) REFERENCES res (id),
    FOREIGN KEY (state) REFERENCES state (slug)
);

DROP TABLE IF EXISTS state_log CASCADE;
CREATE TABLE state_log
(
    id         SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    report     INTEGER,
    state_old  VARCHAR(32),
    state_new  VARCHAR(32),
    FOREIGN KEY (report) REFERENCES report (id),
    FOREIGN KEY (state_old) REFERENCES state (slug),
    FOREIGN KEY (state_old) REFERENCES state (slug)
);
