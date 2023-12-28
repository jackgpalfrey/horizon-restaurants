CREATE TABLE IF NOT EXISTS public.menuitem (
    id uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    name text NOT NULL,
    description text NOT NULL,
    price decimal(12,2) NOT NULL,
    is_available bool NOT NULL DEFAULT TRUE,
    image_url text,
    category_id uuid,
    branch_id uuid NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(id) ON DELETE CASCADE,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES menucategory(id) ON DELETE SET NULL
);
