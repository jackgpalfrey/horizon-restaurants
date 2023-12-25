CREATE TABLE IF NOT EXISTS public.table(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    table_number integer NOT NULL,
    capacity integer,
    branch_id uuid,
    PRIMARY KEY (id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE SET NULL
)