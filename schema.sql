-- Database schema for Webhook + DB Integration Demo
-- Auto-runs on docker-compose up (via init script)

CREATE TABLE IF NOT EXISTS products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    price       NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    stock       INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_products_name ON products USING gin (name gin_trgm_ops);
CREATE INDEX idx_products_desc ON products USING gin (description gin_trgm_ops);

-- Seed data
INSERT INTO products (name, price, stock, description) VALUES
    ('Wireless Bluetooth Headphones', 59.99, 120, 'Over-ear headphones with noise cancellation and 30hr battery life'),
    ('USB-C Hub 7-in-1', 34.99, 200, 'Multi-port adapter with HDMI, USB-A, SD card reader, and PD charging'),
    ('Ergonomic Mouse Pad', 19.99, 350, 'Wrist-rest gel mouse pad with non-slip rubber base'),
    ('Mechanical Keyboard RGB', 89.99, 80, 'Cherry MX Blue switches, full-size, per-key RGB lighting'),
    ('27-inch 4K Monitor', 399.99, 45, 'IPS panel, 99% sRGB, USB-C 65W PD, built-in speakers'),
    ('Portable SSD 1TB', 109.99, 150, 'USB 3.2 Gen 2, read 1050MB/s, write 1000MB/s, IP55 rated'),
    ('Webcam 1080p', 49.99, 95, 'Full HD auto-focus webcam with built-in ring light and privacy shutter'),
    ('Laptop Stand Adjustable', 29.99, 220, 'Aluminium alloy, height adjustable, foldable, ventilated design'),
    ('Smart Desk Lamp', 45.99, 130, 'LED desk lamp with color temperature control, USB charging port'),
    ('Noise Cancelling Earbuds', 79.99, 70, 'True wireless earbuds with ANC, IPX5, 24h total battery life');
