CREATE TABLE IF NOT EXISTS public.table(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    customer_name text NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    guest_num uuid NOT NULL,
    table_id uuid NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_table FOREIGN KEY (table_id) REFERENCES public.table(id) ON DELETE SET NULL
)