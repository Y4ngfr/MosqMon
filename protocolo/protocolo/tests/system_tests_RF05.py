import subprocess
import threading
import pexpect
import time

list_files = False

def init_agent():
	subprocess.run(['python3', 'Agent/Controller.py'])

def service_list_files():
	child = pexpect.spawn('python3 Service/Controller.py')
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("LIST")
	child.expect("Interface do Serviço>".encode("utf-8"))

	files = subprocess.run(['ls', 'audios'], capture_output=True, text=True)

	all_files_list = True
	for file in files.stdout.split("\n"):
		if file not in child.before.decode('utf-8'):
			all_files_list = False
			break

	global list_files
	list_files = all_files_list

def test_system_list_audio_files():
	service_thread = threading.Thread(target=service_list_files)
	agent_thread = threading.Thread(target=init_agent)
	
	service_thread.start()
	time.sleep(2)
	agent_thread.start()
	
	agent_thread.join()
	service_thread.join()
	
	global list_files
	assert list_files