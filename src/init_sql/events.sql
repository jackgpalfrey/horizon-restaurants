CREATE TABLE IF NOT EXISTS public.events
(
    event_id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    branch_id uuid,
    start_time timestamp,
    end_time timestamp,
    type integer NOT NULL,
    phone_number text,
    email text,
    address text,
    PRIMARY KEY (id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE SET NULL
)