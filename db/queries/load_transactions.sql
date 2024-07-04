SELECT
    id,
    user_id,
    title,
    amount,
    date,
    category,
    transaction_type
FROM
    transactions
WHERE
    user_id = ?
