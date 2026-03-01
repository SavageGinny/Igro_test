SELECT
    c.title,
    e.exchange_range,
    to_char(e.created_at, 'DD/MM/YYYY HH24:MI') AS time
FROM exchange_range AS e
JOIN currency AS c ON
    c.currency_id = e.currency_id;