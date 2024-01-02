CREATE TABLE IF NOT EXISTS public.order (
id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
status int NOT NULL DEFAULT 0,
number int NOT NULL,
branch_id uuid NOT NULL,
PRIMARY KEY (id),
CONSTRAINT fk_branch FOREIGN KEY (branch_id) 
    REFERENCES branch(id) ON DELETE CASCADE
)
