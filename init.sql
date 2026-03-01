CREATE TABLE currency(
    currency_id SMALLINT PRIMARY KEY,
    title VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE exchange_range(
    id SERIAL PRIMARY KEY,
    currency_id SMALLINT DEFAULT 1 REFERENCES currency(currency_id),
    exchange_range FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);


INSERT INTO currency (currency_id, title) VALUES
(1, 'USD'),
(2, 'EUR'),
(3, 'CNY'),
(4, 'GBP'),
(5, 'JPY');