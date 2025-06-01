UPDATE
    users
SET
    username = ?,
    fullname = ?,
    photo = ?,
    password_hs = ?,
    salt_pw = ?,
    preferred_currency = ?
WHERE
    id = ?
