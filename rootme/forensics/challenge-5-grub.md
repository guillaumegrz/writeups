### Oh My Grub

` Énoncé
	Votre société a perdu les accès à un ancien serveur, malheureusement celui-ci contient des fichiers importants, à vous de les retrouver.

Files provided : root.ova 

Hypothesis :
- First search what is an ova file
- Search what is grub
- Search if there's a specific CVE for grub or ova files at the time of the challenge (This was a recurrent strat for the precedent challenges)
- I suppose the goal here is to find the access to the machine, such as login and password.
- I will have to look into : Where are data stored in a vm, which parts are accessible without and before login, at what time access control is applied
- I am guessing that maybe the trick here is to find hidden files or hidden access before login to encounter the passwords

### OVA File

An OVA file is a single file archive used to package and distribute VMs and software applications.

To open and use the file I will have to import it in a virtualization program. 

### GRUB

GRUB (Grand Unified Bootloader) is a bootloader program. According to the GRUB doc : Briefly, a _boot loader_ is the first software program that runs when a computer starts. It is responsible for loading and transferring control to an operating system _kernel_ software (such as Linux or GNU Mach). The kernel, in turn, initializes the rest of the operating system (e.g. a GNU system).

I need to know what really happens when grub takes places in the boot chain.

And what does grub allows us to do before the OS protects anything ?

So basically, executes before the OS. So before the authentication, permissions, selinux, secureboot.
It enables modification of boot parameters, editing menu entries, bypassing OS login, loading alternate kernels, and testing system integrity before the operating system’s security policies are active.

- **Modify Kernel Parameters:** By pressing 'e' in the GRUB menu, users can edit commands before booting, such as adding `single` or `init=/bin/bash` to bypass login screens and gain root access.
- **File System Access:** Because GRUB includes its own file-system drivers, it can be used to load custom files or different OS versions, even if the main OS is damaged.
- **Security Measures:** GRUB can be password-protected to prevent unauthorized modification of menu entries. It can also check GPG signatures of kernels to ensure they haven't been tampered with before loading them.

Based on that information, I am going to assume that the grub on this machine isn't protected, and thus can be manipulated to our advantage. the goal here would be to edit some commands before booting to gain root access and explore the machines files to retrieve the required data.

![[Pasted image 20260208193208.png]]

By pressing 'e' on startup, we can enter the grub menu and the boot entry that contains startup info.

![[Pasted image 20260208193841.png]]

This line is very interesting for me. Its the line that basically tells the bootloader where to find the kernel and what settings to apply at startup.

I have changed the 'ro' setting to 'rw', this forced the kernel to mount the drive with full writing permissions immediately. without this, any command run would simply not work because by default, linux boots in readonly mode to check the health of the drive before starting services.

At the end of the line i append the init=/bin/bash command. This tells linux to boot right away to a terminal right on init, and so skip the login parts.
 
![[Pasted image 20260208200119.png]]


This seems to  have worked. I now have root access on the machine. Let's now try to find the required data on the machine to complete the challenge.

In the challenge's description, they are telling that the server contains "important" files. It could be a keyword for the search.

![[Pasted image 20260209230101.png]]

inspecting the /root directory, I could easily retrieve the flag in the .passwd file.

F1aG-M3_PlEas3:)