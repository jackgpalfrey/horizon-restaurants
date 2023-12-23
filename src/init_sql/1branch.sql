CREATE TABLE IF NOT EXISTS public.branch(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    name text NOT NULL UNIQUE,
    address text NOT NULL,
    city_id uuid,
    PRIMARY KEY (id),
    CONSTRAINT fk_city FOREIGN KEY (city_id) REFERENCES city(id) ON DELETE SET NULL
)