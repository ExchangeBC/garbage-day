#This has only been tested with python 2.x

##These dependencies must be installed on machine:

```
sudo pip install Flask Flask-Mail itsdangerous requests
```
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
