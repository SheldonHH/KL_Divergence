\c client3
DROP TABLE IF EXISTS VHashMatrix;
DROP TABLE IF EXISTS DiUnitRange;
DROP TABLE IF EXISTS HashList;

CREATE TABLE VHashMatrix (
                             v_id UUID PRIMARY KEY,
                             row text,
                             col text,
                             vi text[]
);
CREATE TABLE DiUnitRange (
                             d_id serial PRIMARY KEY,
                             unitrange TEXT,
                             di TEXT[]
);
CREATE TABLE HashList (
                          hash_id UUID PRIMARY KEY,
                          rowOrCol TEXT,
                          index integer,
                          concatedResult TEXT,
                          HashResult Integer
);

ALTER TABLE VHashMatrix OWNER TO client3;
ALTER TABLE DiUnitRange OWNER TO client3;
ALTER TABLE HashList OWNER TO client3;

\c client4
DROP TABLE IF EXISTS VHashMatrix;
DROP TABLE IF EXISTS DiUnitRange;
DROP TABLE IF EXISTS HashList;

CREATE TABLE VHashMatrix (
                             v_id UUID PRIMARY KEY,
                             row text,
                             col text,
                             vi text[]
);
CREATE TABLE DiUnitRange (
                             d_id serial PRIMARY KEY,
                             unitrange TEXT,
                             di TEXT[]
);
CREATE TABLE HashList (
                          hash_id UUID PRIMARY KEY,
                          rowOrCol TEXT,
                          index integer,
                          concatedResult TEXT,
                          HashResult Integer
);

ALTER TABLE VHashMatrix OWNER TO client4;
ALTER TABLE DiUnitRange OWNER TO client4;
ALTER TABLE HashList OWNER TO client4;

