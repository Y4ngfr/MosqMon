import subprocess
import threading
import pexpect
import time
from mutagen.wave import WAVE
from mutagen import MutagenError

stop_monitoring = False

def file_is_wav(file_path):
    try:
        audio = WAVE(file_path)  
        return audio.info is not None
    except MutagenError as e:
        return False
    except FileNotFoundError:
        print("Arquivo não encontrado")
        return False

def service_stop_monitoring():
    child = pexpect.spawn('python3 Service/Controller.py')
    child.expect("Interface do Serviço>".encode("utf-8"))
    child.sendline("START_MONITORING 0 3 0")
    child.expect("Interface do Serviço>".encode("utf-8"))
    child.sendline("STOP_MONITORING")
    child.expect("Interface do Serviço>".encode("utf-8"))
    child.sendline("STATUS")
    child.expect("Interface do Serviço>".encode("utf-8"))

    if "Audio Recorder: audio is ready" in child.before.decode('utf-8') and "Data Transporter: ok" in child.before.decode('utf-8'):
        global stop_monitoring
        stop_monitoring = True

def init_agent():
    result = subprocess.run(['python3', 'Agent/Controller.py'])

def test_system_stop_monitoring():
    service_thread = threading.Thread(target=service_stop_monitoring)
    agent_thread = threading.Thread(target=init_agent)

    service_thread.start()
    time.sleep(2)
    agent_thread.start()

    agent_thread.join()
    service_thread.join()

    global stop_monitoring
    assert stop_monitoring