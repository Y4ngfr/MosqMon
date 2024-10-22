import subprocess
import threading
import pexpect
import time

test_missing_params = False
test_invalid_input = False

def service_missing_params():
    expectedMessage = "Erro: forneça 3 parâmetros"

    child = pexpect.spawn('python3 Service/Controller.py')
    child.expect("Interface do Serviço>".encode("utf-8"))
    child.sendline("START_MONITORING 0 1")
    child.expect("Interface do Serviço>".encode("utf-8"))

    if expectedMessage in child.before.decode("utf-8"):
        global test_missing_params
        test_missing_params = True

    child.sendline("CLOSE_CONNECTION")

def service_invalid_input():
    expectedMessage = "Erro: forneça parâmetros válidos (consulte a ajuda)"

    child = pexpect.spawn('python3 Service/Controller.py')
    child.expect("Interface do Serviço>".encode("utf-8"))
    child.sendline("START_MONITORING abc abc abc")
    child.expect("Interface do Serviço>".encode("utf-8"))

    if expectedMessage in child.before.decode("utf-8"):
        global test_invalid_input
        test_invalid_input = True
	
def init_agent():
	result = subprocess.run(['python3', 'Agent/Controller.py'])

def test_system_missing_params_error():
	service_thread = threading.Thread(target=service_missing_params)
	agent_thread = threading.Thread(target=init_agent)
	
	service_thread.start()
	time.sleep(2)
	agent_thread.start()
	
	agent_thread.join()
	service_thread.join()
	
	global test_missing_params
	assert test_missing_params

def test_system_invalid_input_error():
	service_thread = threading.Thread(target=service_invalid_input)
	agent_thread = threading.Thread(target=init_agent)
	
	service_thread.start()
	time.sleep(2)
	agent_thread.start()
	
	agent_thread.join()
	service_thread.join()
	
	global test_invalid_input
	assert test_invalid_input