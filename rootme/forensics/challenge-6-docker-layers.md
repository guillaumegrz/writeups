## Context
```
J’ai perdu le mot de passe pour chiffrer mon fichier de secret. Peux-tu m’aider à le récupérer ?
=> I lost the password to encrypt my secret file. Can you help me recover it ?
```

## Approach and reasoning

Looking at the challenge title, it seems like i'm looking at docker layers. 

What is a docker layer ?
- A layer is a read-only set of file-system changes. 
	Thanks to that info, we could think about recovering some lost data or information in a certain layer
	Every change in the Dockerfile creates a new layer.
	Once built, the image contains the result of the instructions, and every layer is a filesystem, the result of the modified, added, deleted files FROM that step.

How could I 'execute' this image or see what it contains ?
- Based on the previous info I just understood and gathered, i'm not going to need to "execute" the image, but rather find a way to encounter diffs inside the layers, to find which instruction changes have been made, to see if some info has been deleted, or updated in a previous layer for example.

If every archive is a docker version, like a specific step of that docker image, then they must have a chronological order ?

I don´t get why do we keep all the layers, why is the "history"of changes relevant here ? shouldn't we only keep the ¨last state" so to say of the docker file or something ? And build it that way ?
Like, every time you build the image, its gonna tell the instructions like add this, delete that, update that from every layer ? why not keep the "last state"of it ?
- Why keep all the layers ?
	- Docker is made for : reuse, cache, optimization, incremental versioning.
	- If we were to change the last instruction, Docker does not rebuild everything, it reuses the previous layers in cache, and only the last layer (corresponding to the last instruction) changes.
	- If everything was "merged together" or only kept the "last state", every small change would rebuild all the image, which would waste a lot of time.
	- Every instruction, layer, is identified by a hash. If 2 images contains the exact same instruction, they will share the same layer (hash). the layer is stored just once on the disk and then shared between the images that reference its hash.

Docker images are built as a stack of content-addressable filesystem layers, enabling caching and reuse.

With all that info, let's move on. I find in the manifest.json the "structure" of the layers. The tar archives that are being concatenated in a specific order.

## Resolution

Let's decompress all those archives and inspect them one by one to get a closer idea of what's going on.

The ultimate 3 layers are very interesting. in the layer 4, I found a "pass.txt" file. In the layer 5, a "pass.enc" file, and in the layer 6, ".wh.file.txt" 
Which is a special marker used to signify that the file existed in a previous layer and has been deleted. Interesting. I can assume that the pass has been created or stored in layer 4, encrypted in layer 5, and the original file deleted in layer 6.

Since the challenge is about encountering the pass to encrypt the Docker secret, I know have a crucial piece of info, that pass.txt file, that I suppose can be used to decrypt the secret file.

I now have to find the secret file in those archives, or find a way to decode the pass.enc file.

I found at the root of the folder a json file containing all the instruction used in every layer.

There is the command used to encrypt the file. Lets try to use these info to decrypt the flag.enc file then.

```openssl enc -aes-256-cbc -iter 10 -pass pass:$(cat /pass.txt) -out flag.enc```

Here they encrypted an encrypted password "flag.enc" using the aes-256-cbc algorithm, with 10 iterations and the flag.txt password, which I assume adds salt or complexity to the final encryption.

Since i have all the info, I can use the command to decrypt the flag.enc file, using the same password stored in pass.txt, with the same iterations and algorithm used.

There it is. the -d option means decrypt. Since the end goal is to decrypt here, we use the .enc as input. The output will be our decrypted password.

## Flag

`>openssl enc -d -aes-256-cbc -iter 10 -in flag.enc -out decrypted.txt -pass pass:$(cat pass.txt)
`>cat decrypted.txt

## Conclusion

This challenge demonstrates how secrets accidentally stored in intermediate Docker layers remain recoverable, even if deleted in later layers.


