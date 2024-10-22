import subprocess
import threading
import pexpect
import time
from mutagen.wave import WAVE
from mutagen import MutagenError

status = False

def service_status():
	child = pexpect.spawn('python3 Service/Controller.py')
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("STATUS")
	child.expect("Interface do Serviço>".encode("utf-8"))
	
	if "Audio Recorder: audio is ready" in child.before.decode('utf-8') and "Data Transporter: ok" in child.before.decode('utf-8'):
		global status
		status = True

def init_agent():
	subprocess.run(['python3', 'Agent/Controller.py'])

def test_system_status():
	service_thread = threading.Thread(target=service_status)
	agent_thread = threading.Thread(target=init_agent)
	
	service_thread.start()
	time.sleep(2)
	agent_thread.start()
	
	agent_thread.join()
	service_thread.join()
	
	global status
	assert status