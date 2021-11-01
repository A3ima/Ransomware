# Ransomware
In this project I created a Ransomware with Python.
I used advanced VM evasion techniques, combined with a very strong encryption.

# Evading VM and Sandbox
* Checking for Physics components like: Fans, CPU Temperature...
* Checking for Registry keys, certain files that represent we are running on VM.
* Checking for certain MAC addresses.
* Checking for running services and tasks.
* Checking for mouse movement.
* Sleeping for a certain amount of time.

# Encryption
We are using a 512 bits key with AES encryption (Decrypting 256 key would approximatly take 2.29 * 10^32 years).
We are also using what's called the RIPlace technique, to avoid AV detection.
[See more about RIPlace](https://www.bleepingcomputer.com/news/security/new-riplace-bypass-evades-windows-10-av-ransomware-protection/)

# How the Ransomware works
First the program checks if it's already run by checking for certain registry key and file.
If it's the first time it runs, it will evade detection by doing the checks above, and finally wait for a certain amount of time.
Once it's done waiting, it copies it self to the Startup folder, adds a new Registry key, and then it restarts into Safe Mode without network connection (Studies found that most AV don't run properly on Safe Mode).

Once the computer is on Safe Mode, it starts encrypting the files, and adding note on the Desktop to explain the user what to do.

# Note
This project doesn't allow to decrypt the data back, while it tells the user it can.
So don't look for the decrypt method.

# Disclaimer
## USE THIS PROJECT FOR EDUCATIONAL PURPOSES ONLY. THIS IS A VERY HARMFUL PROJECT WITH NO OPTION TO RETURN BACK THE DATA.
## I AM NOT RESPONSIBLE FOR ANYTHING YOU DO WITH THIS PROJECT.
