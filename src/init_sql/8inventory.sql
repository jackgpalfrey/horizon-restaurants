CREATE TABLE IF NOT EXISTS public.inventory(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    name text NOT NULL UNIQUE,
    quantity integer NOT NULL,
    threshold integer,
    branch_id uuid NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES public.branch(id) ON DELETE SET NULL
)