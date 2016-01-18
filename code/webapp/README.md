#This has only been tested with python 2.x

##These dependencies must be installed on machine:

sudo pip install Flask
sudo pip install Flask-Mail
sudo pip install itsdangerous

##Further configuration for mysql database:

```
CREATE DATABASE garbageday;

CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 email VARCHAR(100),
 address varchar(255),
 zone INT,
confirmed BOOLEAN NOT NULL DEFAULT 0);

CREATE TABLE zones (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 pickupdate DATETIME,
 zone INT);
```

-------------------------------------------------------------------------

```
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_email VARCHAR(255),
    IN p_zone VARCHAR(255)
)
BEGIN
    if ( select exists (select 1 from users where email = p_email) ) THEN

        select 'Email has already been used!';

    ELSE

        insert into users
        (
            email,
            zone
        )
        values
        (
            p_email,
            p_zone
        );

    END IF;
END$$
DELIMITER ;
````
