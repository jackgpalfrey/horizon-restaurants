CREATE TABLE IF NOT EXISTS public.branchstaff(
    user_id uuid NOT NULL UNIQUE,
    branch_id uuid NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES staff(id) ON DELETE CASCADE,
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE CASCADE
)
