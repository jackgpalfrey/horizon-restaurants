CREATE TABLE IF NOT EXISTS public.events
(
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    branch_id uuid NOT NULL,
    start_time timestamp NOT NULL,
    end_time timestamp NOT NULL,
    type integer NOT NULL,
    phone_number text,
    email text,
    address text,
    order_id uuid UNIQUE,
    PRIMARY KEY (id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE CASCADE,
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES public.order(id) ON DELETE SET NULL
)
