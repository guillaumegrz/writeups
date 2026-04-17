#### About

Vaccine is a very easy Linux machine that emphasizes enumeration and password cracking. Anonymous FTP access exposes a password-protected backup archive which can be cracked to recover web application credentials. These credentials grant access to a PHP application vulnerable to SQL injection which leads to command execution and an initial shell as the postgres user. Finally, privilege escalation can be achieved by abusing misconfigured sudo permissions on vi.

- - - 

>Besides SSH and HTTP, what other service is hosted on this box?
>`FTP`
>
```bash
> nmap 10.129.95.174
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-04-15 10:04 -03
Nmap scan report for 10.129.95.174
Host is up (0.21s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 23.32 seconds

```

>This service can be configured to allow login with any password for specific username. What is that username?
>`anonymous`
```bash
> ftp 10.129.95.174
Connected to 10.129.95.174.
220 (vsFTPd 3.0.3)
Name (10.129.95.174:guillaume): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||10489|)
150 Here comes the directory listing.
-rwxr-xr-x    1 0        0            2533 Apr 13  2021 backup.zip
226 Directory send OK.
ftp> 
```

>What script comes with the John The Ripper toolset and generates a hash from a password protected zip archive in a format to allow for cracking attempts?

