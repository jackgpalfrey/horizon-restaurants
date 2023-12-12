CREATE TABLE branch (
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    name text NOT NULL,
    address text NOT NULL,
    PRIMARY KEY (id)
)