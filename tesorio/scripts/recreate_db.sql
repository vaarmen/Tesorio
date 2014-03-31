

# http://stackoverflow.com/questions/11170133/using-mysql-with-django-access-denied-for-user-localhost
# mysql -u root -p < scripts/script.sql

#-- Steps to update/clear database:
#-- 1. Use above mysql command
#-- 2. sync with ./manage.py syncdb
#-- 3. migrate with  ./manage.py migrate app

DROP DATABASE IF EXISTS `tesorio1_local`;
CREATE DATABASE `tesorio1_local`
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;

USE 'mysql';
GRANT ALL PRIVILEGES ON tesorio1_local.* TO 'root'@'localhost'

WITH GRANT OPTION;
FLUSH PRIVILEGES;
