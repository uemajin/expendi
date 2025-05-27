SELECT
    id,
    username,
    fullname,
    password_hs,
    salt_pw,
    photo
FROM
    users
WHERE
    username = ?