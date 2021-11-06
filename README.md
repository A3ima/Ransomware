# Ransomware
In this project I created a Ransomware with Python.
I used advanced VM evasion techniques, combined with a very strong encryption.

# Evading VM and Sandbox
* Checking for Physics components like: Fans, CPU cores...
* Checking for Registry keys and certain files.
* Checking for certain MAC addresses.
* Checking for running services and tasks.
* Checking for mouse movement.

# Encryption
We are using a 512 bits key with RSA encryption (Decrypting 256 key would approximatly take 2.29 * 10^32 years).
We are also using what's called the RIPlace technique, to avoid AV detection.
[See more about RIPlace.](https://www.bleepingcomputer.com/news/security/new-riplace-bypass-evades-windows-10-av-ransomware-protection/)

# How the Ransomware works
First the program checks if it's already run by checking if a registry key and file exists.
If yes, it will start the ransomware, which means Generating 512 bits key, encrypting everything, adding a note to the user and shredding itself from the system.

else it will evade detection by doing the checks above, once it's done it will write itself to the registry and reboot into safe mode.

If the program detects VM or some test environment, it will shred itself from the system.

# Note
To properly run this project, you need Administrator Privileges (because we are writing to the Registry), so if you remove it, it can be executed without those privileges.

This project doesn't allow to decrypt the data back, while it tells the user it can, so don't look for the decrypt method.
As soon as it's done encrypting the system it will delete itself.

# To Do
* Use the RIPlace method.
* Spread across the network.

# Disclaimer
### USE THIS PROJECT FOR EDUCATIONAL PURPOSES ONLY. THIS IS A VERY HARMFUL PROJECT WITH NO OPTION TO RETRIEVE THE DATA ONCE EXECUTED.
### I AM NOT RESPONSIBLE FOR ANYTHING YOU DO WITH THIS PROJECT.
