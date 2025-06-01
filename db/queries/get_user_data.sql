SELECT
    id,
    username,
    fullname,
    password_hs,
    salt_pw,
    photo,
    preferred_currency
FROM
    users
WHERE
    username = ?