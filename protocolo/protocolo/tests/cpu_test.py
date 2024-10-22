from memory_profiler import profile
import subprocess
import threading
import pexpect
import time
import psutil
from mutagen.wave import WAVE
from mutagen import MutagenError

# Variáveis Globais
pull_audio = False
incorrect_name_test = False
output = ""
cpu_usage = []
memory_usage = []
network_usage_start = None
monitoring = True  # Controle para parar monitoramento

# Verifica se o arquivo é um WAV válido
@profile
def file_is_wav(file_path):
    try:
        audio = WAVE(file_path)
        return audio.info is not None
    except (MutagenError, FileNotFoundError):
        print(f"Erro ao abrir o arquivo: {file_path}")
        return False

# Inicia o Agente
@profile
def init_agent():
    subprocess.run(['python3', 'Agent/Controller.py'])

# Serviço para capturar áudio e medir latência
@profile
def service_pull_audio():
    global output, pull_audio

    child = pexpect.spawn('python3 Service/Controller.py')
    child.expect("Interface do Serviço>".encode("utf-8"))

    # Marca tempo de envio do comando e resposta (latência)
    start_time = time.perf_counter()
    child.sendline('PULL_AUDIO "audioFile.wav"')
    child.expect("Interface do Serviço>".encode("utf-8") )
    end_time = time.perf_counter()

    latency = end_time - start_time
    print(f"Latência de PULL_AUDIO: {latency:.4f} segundos")

    child.sendline("CLOSE_CONNECTION")
    output = child.before.decode("utf-8")

    if file_is_wav("correspondencia/audioFile.wav"):
        pull_audio = True

# Testa nome de arquivo incorreto
@profile
def service_incorrect_name_test():
    EXPECTED_OUTPUT = "[Errno 21] Is a directory: 'audios/'"
    child = pexpect.spawn('python3 Service/Controller.py')
    child.expect("Interface do Serviço>".encode("utf-8"))

    start_time = time.perf_counter()  # Tempo de envio do comando
    child.sendline("PULL_AUDIO \" \"")
    child.expect("Interface do Serviço>".encode("utf-8"))
    end_time = time.perf_counter()
    child.sendline("STATUS")
    child.expect("Interface do Serviço>".encode("utf-8"))

    latency = end_time - start_time
    print(f"Latência de comando inválido: {latency:.4f} segundos")
    # print(child.before.decode("utf-8"))

    if EXPECTED_OUTPUT in child.before.decode("utf-8"):
        global incorrect_name_test
        incorrect_name_test = True

# Monitoramento de recursos (CPU, memória e rede)
@profile
def monitor_resources():
    global cpu_usage, memory_usage, network_usage_start, monitoring

    # Captura o estado inicial da rede
    network_usage_start = psutil.net_io_counters()

    while monitoring:
        cpu_usage.append(psutil.cpu_percent(interval=1))
        memory_usage.append(psutil.virtual_memory().percent)
        time.sleep(1)  # Ajustar conforme necessário

# Gera relatório de desempenho e overhead
@profile
def generate_report():
    global network_usage_start

    # Captura o estado final da rede
    network_usage_end = psutil.net_io_counters()
    bytes_sent = network_usage_end.bytes_sent - network_usage_start.bytes_sent
    bytes_recv = network_usage_end.bytes_recv - network_usage_start.bytes_recv

    print("\n--- Relatório de Desempenho ---")
    print(f"Uso médio de CPU: {sum(cpu_usage) / len(cpu_usage):.2f}%")
    print(f"Uso médio de Memória: {sum(memory_usage) / len(memory_usage):.2f}%")
    print(f"Bytes enviados: {bytes_sent}")
    print(f"Bytes recebidos: {bytes_recv}")

# Teste de integridade dos dados
@profile
def test_system_data_integrity():
    EXPECTED_MSG = "Integridade verificada com sucesso!"
    assert EXPECTED_MSG in output, "Falha na verificação de integridade"

@profile
def test_system_get_audio_file_with_incorrect_name():
    service_thread = threading.Thread(target=service_incorrect_name_test)
    agent_thread = threading.Thread(target=init_agent)

    start_time = time.perf_counter()

    service_thread.start()
    time.sleep(2)
    agent_thread.start()

    agent_thread.join()
    service_thread.join()

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    global incorrect_name_test

    assert incorrect_name_test, "Falha ao detectar erro de nome incorreto"
    print(f"Tempo de execução: {elapsed_time:.2f} segundos")


# Teste de captura de áudio com monitoramento
@profile
def test_system_pull_audio():
    global monitoring

    # Inicia monitoramento em thread separada
    monitor_thread = threading.Thread(target=monitor_resources)
    monitor_thread.start()

    # Threads para serviço e agente
    service_thread = threading.Thread(target=service_pull_audio)
    agent_thread = threading.Thread(target=init_agent)

    start_time = time.perf_counter()

    service_thread.start()
    time.sleep(2)  # Aguarda serviço iniciar
    agent_thread.start()

    agent_thread.join()
    service_thread.join()

    # Parar monitoramento
    monitoring = False
    monitor_thread.join()

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    assert pull_audio, "Falha ao capturar o áudio"
    print(f"Tempo total de execução: {elapsed_time:.2f} segundos")
    generate_report()

# Execução dos testes
if __name__ == "__main__":
    print("Iniciando teste de pull de áudio...")
    test_system_pull_audio()

    print("\nVerificando integridade dos dados...")
    test_system_data_integrity()

    print("\nIniciando teste de nome incorreto...")
    test_system_get_audio_file_with_incorrect_name()
