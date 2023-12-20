CREATE TABLE IF NOT EXISTS public.MenuCategory(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    branch_id uuid NOT NULL,
    name text NOT NULL UNIQUE,  
    PRIMARY KEY (id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES public.Branch(id) ON DELETE CASCADE
)
