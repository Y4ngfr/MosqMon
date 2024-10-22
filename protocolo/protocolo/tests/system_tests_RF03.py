import subprocess
import threading
import pexpect
import time
import sys
from mutagen.wave import WAVE
from mutagen import MutagenError

pull_audio = False
incorrect_name_test = False
output = ""

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

def service_pull_audio():
	child = pexpect.spawn('python3 Service/Controller.py')
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("PULL_AUDIO \"audioFile.wav\"")
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("CLOSE_CONNECTION")

	global output
	output = child.before.decode("utf-8")
	
	if file_is_wav("correspondencia/audioFile.wav"):
		global pull_audio
		pull_audio = True

def service_incorrect_name_test():
	EXPECTED_OUTPUT = "[Errno 21] Is a directory: \'audios/\'"
	child = pexpect.spawn('python3 Service/Controller.py')
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("PULL_AUDIO \" \"")
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("STATUS")
	child.expect("Interface do Serviço>".encode("utf-8"))

	if EXPECTED_OUTPUT in child.before.decode("utf-8"):
		global incorrect_name_test
		incorrect_name_test = True

def test_system_pull_audio():
	service_thread = threading.Thread(target=service_pull_audio)
	agent_thread = threading.Thread(target=init_agent)
	
	service_thread.start()
	time.sleep(2)
	agent_thread.start()
	
	agent_thread.join()
	service_thread.join()
	
	global pull_audio
	assert pull_audio

def test_system_get_audio_file_with_incorrect_name():
	service_thread = threading.Thread(target=service_incorrect_name_test)
	agent_thread = threading.Thread(target=init_agent)
	
	service_thread.start()
	time.sleep(2)
	agent_thread.start()
	
	agent_thread.join()
	service_thread.join()
	
	global incorrect_name_test
	assert incorrect_name_test

def test_system_data_integrity():
	EXPECTED_MSG = "Integridade verificada com sucesso!"
	global output
	assert EXPECTED_MSG in output