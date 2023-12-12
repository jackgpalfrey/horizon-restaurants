CREATE TABLE IF NOT EXISTS branch(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    name text NOT NULL UNIQUE,
    address text NOT NULL,
    PRIMARY KEY (id)
)