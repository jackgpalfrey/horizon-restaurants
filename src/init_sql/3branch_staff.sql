CREATE TABLE IF NOT EXISTS public.branchstaff(
    user_id uuid,
    branch_id uuid NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES staff(id) ON DELETE SET NULL,
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE SET NULL
)