import subprocess
import threading
import pexpect
import time
from mutagen.wave import WAVE
from mutagen import MutagenError

rename_file = False
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

def service_rename_file():
	child = pexpect.spawn('python3 Service/Controller.py')
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("RENAME 0 \"audioFile.wav\"")
	child.expect("Interface do Serviço>".encode("utf-8"))
	
	if "File audio" in child.before.decode('utf-8') and \
    	"renamed to: audioFile.wav" in child.before.decode('utf-8') and\
		file_is_wav("correspondencia/audioFile.wav"):
			global rename_file
			rename_file = True

def service_incorrect_name_test():
	EXPECTED_OUTPUT = "[Errno 2] No such file or directory: \'audios/ \' -> \'audios/ \'"

	child = pexpect.spawn('python3 Service/Controller.py')
	child.expect("Interface do Serviço>".encode("utf-8"))
	child.sendline("RENAME \" \" \" \"")
	child.expect("Interface do Serviço>".encode("utf-8"))

	if EXPECTED_OUTPUT in child.before.decode("utf-8"):
		global incorrect_name_test
		incorrect_name_test = True

def test_system_rename_audio_file():
	service_thread = threading.Thread(target=service_rename_file)
	agent_thread = threading.Thread(target=init_agent)
	
	service_thread.start()
	time.sleep(2)
	agent_thread.start()
	
	agent_thread.join()
	service_thread.join()
	
	global rename_file
	assert rename_file

def test_system_rename_file_with_incorrect_name():
	service_thread = threading.Thread(target=service_incorrect_name_test)
	agent_thread = threading.Thread(target=init_agent)
	
	service_thread.start()
	time.sleep(2)
	agent_thread.start()
	
	agent_thread.join()
	service_thread.join()
	
	global incorrect_name_test
	assert incorrect_name_test