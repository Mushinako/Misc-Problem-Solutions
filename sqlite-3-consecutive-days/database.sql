SELECT name
FROM logins n
WHERE
    EXISTS(
        SELECT 1
        FROM logins
        WHERE
            name=n.name
            AND
            date(last_login_date)=date(n.last_login_date, "+1 day")
    )
    AND
    EXISTS(
        SELECT 1
        FROM logins
        WHERE 
            name=n.name
            AND
            date(last_login_date)=date(n.last_login_date, "+2 day")
    )

