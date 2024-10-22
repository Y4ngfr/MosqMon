import subprocess
import threading
import pexpect
import time
from mutagen.wave import WAVE
from mutagen import MutagenError

start_monitoring = False

def file_is_wav(file_path):
		try:
			audio = WAVE(file_path)  
			return audio.info is not None
		except MutagenError as e:
			return False
		except FileNotFoundError:
			print("Arquivo não encontrado")
			return False

def service_start_monitoring():
	child = pexpect.spawn('python3 Service/Controller.py')
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("START_MONITORING 0 1 3")
	child.expect("Interface do Serviço>".encode("utf-8"))
	
def agent_start_monitoring():
	result = subprocess.run(['python3', 'Agent/Controller.py'], capture_output=True, text=True)
	
	if file_is_wav(result.stdout.split("\n")[0]):
		global start_monitoring
		start_monitoring = True

def test_system_start_monitoring():
	service_thread = threading.Thread(target=service_start_monitoring)
	agent_thread = threading.Thread(target=agent_start_monitoring)
	
	service_thread.start()
	time.sleep(2)
	agent_thread.start()
	
	agent_thread.join()
	service_thread.join()
	
	global start_monitoring
	assert start_monitoring