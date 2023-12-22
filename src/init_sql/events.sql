CREATE TABLE IF NOT EXISTS public.events
(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    branch_id uuid,
    start_time timestamp NOT NULL,
    end_time timestamp NOT NULL,
    type integer NOT NULL,
    phone_number text NOT NULL,
    email text NOT NULL,
    address text,
    PRIMARY KEY (id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE SET NULL
)