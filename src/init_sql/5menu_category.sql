CREATE TABLE IF NOT EXISTS public.menucategory (
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    name text NOT NULL,
    branch_id uuid NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE CASCADE
);
