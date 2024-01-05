CREATE TABLE IF NOT EXISTS public.orderitem(
    order_id uuid NOT NULL,
    item_id uuid NOT NULL,
    quantity int NOT NULL,
    CONSTRAINT fk_item FOREIGN KEY (item_id) REFERENCES menuitem(id) ON DELETE CASCADE,
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES public.order(id) ON DELETE CASCADE
)
