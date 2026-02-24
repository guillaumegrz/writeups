
#### Énoncé

	Le chat du président a été kidnappé par des indépendantistes. Un suspect a été interpellé par la gendarmerie. Il détenait sur lui une clef USB. Berthier, une nouvelle fois, à vous de jouer ! Essayez de faire parler cette clef et de trouver dans quelle ville est retenu ce chat !
	Le flag est le nom de la ville en minuscule.

We are presented with a "chall9" binary file without any extension, and a document "Tutorial on Disk Drive Data Sanitization"

```bash
> file chall9
chall9: DOS/MBR boot sector; partition 1 : ID=0xb, start-CHS (0x0,32,33), end-CHS (0x10,81,1), startsector 2048, 260096 sectors, extended partition table (last)
```

This is a MBR boot partition.

I am going to mount the archive at the specific offset. 
Start sector = 2048 * 512 bytes = offset = 1048576

```bash
sudo mount -o loop,offset=1048576 chall9 /mnt
```

> ll /mnt
total 5.0K
drwxr-xr-x 2 root root 1.5K Jul 22  2013 Documentations
drwxr-xr-x 2 root root 1.0K Jul 22  2013 Files
drwxr-xr-x 7 root root 2.5K Jul 22  2013 WebSites

This looks like some archives containing a lot of different documents, and files. The goal here is to find a city where a cat disappeared. The mounted archives is supposed to be a USB stick found on a suspect.

My first idea is that this is a pure detective challenge, meaning finding some kind of evidence just exploring the archive and files.

The names of saved Websites : 
- Apple iPhone 4 specs
- **L'autonomie de l'Alsace**
- **République d'Alsace-Lorraine**
- Sept façons de tuer un chat
- **Voyager avec un chat**

We start having a profile of the suspect.

There also is a 'Files' directory containing Word files.
- > find ./Files -type f | sort
	./Files/421_20080208011.doc
	./Files/Coker.doc
	./Files/Creer_votre_association.doc
	./Files/DataSanitizationTutorial.odt

Let's inspect those files' metadatas to try and get some more info on the authors, 

-  ./Files/421_20080208011.doc 
	- Author : Jean-marie naas
	- Last modified by : jojanneke.kramer
	- Company : MDLF
- ./Files/Coker.doc
	- Author : Amanda Lee Coker
	- Last modified : Amanda Lee Coker
- ./Files/Creer_votre_association.doc
	- Author : cyrille
	- Last modified : cyrille
	- Bytes : cyrille.pilleniere@wanadoo.fr
- ./Files/DataSanitizationTutorial.odt
	- Creator : Trust:

Nothing really convincing inside the mounted files.

Let's try to do some file carving on the image. File carving is a raw reading of the binary. It reads the disk sector by sector like a raw byte sequence. It does not ask the system file what exists or no. It search the signatures, which are specific byte sequences defined by its standard. For example :

```
JPEG : FF D8 FF E0 ... 
PNG : 89 50 4E 47 0D 0A 1A 0A (-> 89 PNG \r\n in ASCII) 
PDF : 25 50 44 46 (-> %PDF in ASCII) 
ZIP : 50 4B 03 04 (-> PK in ASCII) 
ODT : 50 4B 03 04 (a ODT is a ZIP, same signature) 
DOCX : 50 4B 03 04 (same, all modern office formats are ZIPs)
```

When you mount the image, like I did, it uses the file system, FAT, NTFS... It reads the index. It tells you "here are the files that exists". When a file is deleted, the index tells that 'this space is free' and the file disappears from the mounted view. Physically, the data is still here, but the index doesn't reference them anymore.

Lets extract the ODT file found in the photorec extract.
```bash
> cp recup_dir.1/f0019458.odt /tmp/revendication.zip
> unzip /tmp/revendication.zip -d /tmp/odt_content
Archive:  /tmp/revendication.zip
 extracting: /tmp/odt_content/mimetype  
 extracting: /tmp/odt_content/Thumbnails/thumbnail.png  
  inflating: /tmp/odt_content/Pictures/1000000000000CC000000990038D2A62.jpg  
  inflating: /tmp/odt_content/content.xml  
  inflating: /tmp/odt_content/styles.xml  
  inflating: /tmp/odt_content/settings.xml  
  inflating: /tmp/odt_content/meta.xml  
  inflating: /tmp/odt_content/manifest.rdf  
  inflating: /tmp/odt_content/Configurations2/accelerator/current.xml  
   creating: /tmp/odt_content/Configurations2/toolpanel/
   creating: /tmp/odt_content/Configurations2/statusbar/
   creating: /tmp/odt_content/Configurations2/progressbar/
   creating: /tmp/odt_content/Configurations2/toolbar/
   creating: /tmp/odt_content/Configurations2/images/Bitmaps/
   creating: /tmp/odt_content/Configurations2/popupmenu/
   creating: /tmp/odt_content/Configurations2/floater/
   creating: /tmp/odt_content/Configurations2/menubar/
  inflating: /tmp/odt_content/META-INF/manifest.xml  

```

The ODT archive contains a picture, lets look at the exif data to find the GPS data.

```bash
> ls /tmp/odt_content/Pictures
1000000000000CC000000990038D2A62.jpg
> exiftool /tmp/odt_content/Pictures/*
ExifTool Version Number         : 12.76
File Name                       : 1000000000000CC000000990038D2A62.jpg
Directory                       : /tmp/odt_content/Pictures
File Size                       : 2.3 MB
File Modification Date/Time     : 2013:07:22 21:25:22-04:00
File Access Date/Time           : 2013:07:22 21:25:22-04:00
File Inode Change Date/Time     : 2026:02:24 17:42:51-03:00
File Permissions                : -rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
Exif Byte Order                 : Big-endian (Motorola, MM)
Make                            : Apple
Camera Model Name               : iPhone 4S
Orientation                     : Horizontal (normal)
X Resolution                    : 72
Y Resolution                    : 72
Resolution Unit                 : inches
Software                        : 6.1.2
Modify Date                     : 2013:03:11 11:47:07
Y Cb Cr Positioning             : Centered
Exposure Time                   : 1/20
F Number                        : 2.4
Exposure Program                : Program AE
ISO                             : 160
Exif Version                    : 0221
Date/Time Original              : 2013:03:11 11:47:07
Create Date                     : 2013:03:11 11:47:07
Components Configuration        : Y, Cb, Cr, -
Shutter Speed Value             : 1/20
Aperture Value                  : 2.4
Brightness Value                : 1.477742947
Metering Mode                   : Multi-segment
Flash                           : Off, Did not fire
Focal Length                    : 4.3 mm
Subject Area                    : 1631 1223 881 881
Flashpix Version                : 0100
Color Space                     : sRGB
Exif Image Width                : 3264
Exif Image Height               : 2448
Sensing Method                  : One-chip color area
Exposure Mode                   : Auto
White Balance                   : Auto
Focal Length In 35mm Format     : 35 mm
Scene Capture Type              : Standard
GPS Latitude Ref                : North
GPS Longitude Ref               : East
GPS Altitude Ref                : Above Sea Level
GPS Time Stamp                  : 07:46:50.85
GPS Img Direction Ref           : True North
GPS Img Direction               : 247.3508772
Compression                     : JPEG (old-style)
Thumbnail Offset                : 902
Thumbnail Length                : 8207
Image Width                     : 3264
Image Height                    : 2448
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Aperture                        : 2.4
Image Size                      : 3264x2448
Megapixels                      : 8.0
Scale Factor To 35 mm Equivalent: 8.2
Shutter Speed                   : 1/20
Thumbnail Image                 : (Binary data 8207 bytes, use -b option to extract)
GPS Altitude                    : 16.7 m Above Sea Level
GPS Latitude                    : 47 deg 36' 16.15" N
GPS Longitude                   : 7 deg 24' 52.48" E
Circle Of Confusion             : 0.004 mm
Field Of View                   : 54.4 deg
Focal Length                    : 4.3 mm (35 mm equivalent: 35.0 mm)
GPS Position                    : 47 deg 36' 16.15" N, 7 deg 24' 52.48" E
Hyperfocal Distance             : 2.08 m
Light Value                     : 6.2

```

With a basic search on google maps with the GPS coordinates, we easily find the city name which is the flag.
