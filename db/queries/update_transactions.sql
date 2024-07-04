UPDATE transactions
SET user_id = ?,
    title = ?,
    amount = ?,
    date = ?,
    category = ?,
    transaction_type = ?
WHERE id = ?
