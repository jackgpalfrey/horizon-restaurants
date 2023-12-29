CREATE TABLE IF NOT EXISTS public.discounts(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    multiplier decimal(3,2),
    description text,    
    branch_id uuid,
    PRIMARY KEY (id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE SET NULL
)