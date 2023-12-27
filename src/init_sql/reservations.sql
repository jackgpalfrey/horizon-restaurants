CREATE TABLE IF NOT EXISTS public.reservations(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    customer_name text NOT NULL,
    reservation_time TIMESTAMP NOT NULL,
    end_time TIME NOT NULL,
    guest_num integer NOT NULL,
    table_id uuid NOT NULL,
    branch_id uuid NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_table FOREIGN KEY (table_id) REFERENCES public.table(id) ON DELETE SET NULL,
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES public.branch(id) ON DELETE SET NULL
)