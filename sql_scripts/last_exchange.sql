SELECT
    c.title,
    e.exchange_range
FROM exchange_range AS e
JOIN currency AS c ON
    c.currency_id = e.currency_id
WHERE e.created_at = (
    SELECT MAX(created_at)
    FROM exchange_range
    );