import subprocess
import threading
import pexpect
import time
import os
from mutagen.wave import WAVE
from mutagen import MutagenError

remove_file = False
incorrect_name_test = False

def file_is_wav(file_path):
        try:
            audio = WAVE(file_path)  
            return audio.info is not None
        except MutagenError as e:
            return False
        except FileNotFoundError:
            print("Arquivo não encontrado")
            return False

def init_agent():
	subprocess.run(['python3', 'Agent/Controller.py'])

def service_remove_file():
	files = os.listdir("audios")

	child = pexpect.spawn('python3 Service/Controller.py')
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("DELETE 0")
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("CLOSE_CONNECTION")

	fileName = files[0]
	
	if f"file deleted: {fileName}" in child.before.decode('utf-8') and \
        not file_is_wav(fileName):
		global remove_file
		remove_file = True	

def service_incorrect_name_test():
	EXPECTED_OUTPUT = "[Errno 2] No such file or directory: \'audios/ \'"

	child = pexpect.spawn('python3 Service/Controller.py')
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("DELETE \" \"")
	child.expect("Interface do Serviço>".encode("utf-8"))

	if EXPECTED_OUTPUT in child.before.decode("utf-8"):
		global incorrect_name_test
		incorrect_name_test = True

def test_system_remove_audio_file():
	service_thread = threading.Thread(target=service_remove_file)
	agent_thread = threading.Thread(target=init_agent)
	
	service_thread.start()
	time.sleep(2)
	agent_thread.start()
	
	agent_thread.join()
	service_thread.join()
	
	global remove_file
	assert remove_file

def test_system_remove_file_with_incorrect_name():
	service_thread = threading.Thread(target=service_incorrect_name_test)
	agent_thread = threading.Thread(target=init_agent)
	
	service_thread.start()
	time.sleep(2)
	agent_thread.start()
	
	agent_thread.join()
	service_thread.join()
	
	global incorrect_name_test
	assert incorrect_name_test