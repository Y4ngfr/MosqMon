import pytest
import subprocess
from mutagen.wave import WAVE
from mutagen import MutagenError

def file_is_wav(file_path):
        try:
            audio = WAVE(file_path)  
            return audio.info is not None
        except MutagenError as e:
            return False
        except FileNotFoundError:
            print("Arquivo não encontrado")
            return False

def test_audio_recording_with_3_repetitions():
    result = subprocess.run(['./../audioRecorder', '-i0', '-t2', '-r3', '-o../recordings'], capture_output=True, text=True)
    saida = result.stdout.split("\n")[:-1]

    verify = True        

    for arquivo in saida:        
        if file_is_wav(str(arquivo)) == False:
            verify = False

    assert verify == True

def test_audio_recording_with_float_number_param():
    result = subprocess.run(['./../audioRecorder', '-i0', '-t3.999999', '-r1', '-o../recordings'], capture_output=True, text=True)
    saida = result.stdout.split("\n")[:-1]

    verify = True        

    for arquivo in saida:        
        if file_is_wav(arquivo) == False:
            verify = False

    assert verify

def test_audio_recording_with_time_less_than_1():
    result = subprocess.run(['./../audioRecorder', '-i0', '-t0.345', '-r5', '-o../recordings'], capture_output=True, text=True)
    saida = result.stdout.split("\n")[:-1]

    verify = True        

    for arquivo in saida:        
        if file_is_wav(arquivo) == False:
            verify = False

    assert verify

def test_help_message():
	EXPECTED_OUTPUT = "Uso: audioRecorder [options] file...\nOptions:\n--help                       Mostra informações de ajuda\n--devices                    Lista os dispositivos de gravação\n-t <arg>                     Define o tempo de gravação em segundos\n-o <directory>               Define o diretório de saída\n-r <arg>                     Define quantas vezes a gravação se repete (definir como 0 para repetir indefinidamente)\n-i <arg>                     Define o índice do dispositivo de gravação\nExemplo: gravador -i 0 -o meu/diretorio/ -t 5 -r 10\nGrava 10 áudios de 5 segundos com o dispositivo de gravação 0 e coloca em meu/diretorio\n"
	result = subprocess.run(['./../audioRecorder', '--help'], capture_output=True, text=True)
		
	assert result.stdout == EXPECTED_OUTPUT

def test_file_not_found_error():
    result = subprocess.run(['./../audioRecorder', '-i0', '-t0.345', '-r5', '-o../ \n'], capture_output=True, text=True)
    saida = result.stdout.split("\n")[:-1]

    verify = True        

    for arquivo in saida:        
        if file_is_wav(arquivo) == False:
            verify = False

    assert not verify

def test_invalid_input_error():
    EXPECTED_OUTPUT = "Opção `-t` não reconhecida\n"
    result = subprocess.run(['./../audioRecorder', '-i0', '-t'], capture_output=True, text=True)
    
    assert EXPECTED_OUTPUT == result.stdout

def test_missing_params_error():
    EXPECTED_OUTPUT = "Erro: argumento -r ausente\nErro: argumento -o ausente\n"
    result = subprocess.run(['./../audioRecorder', '-i0', '-t4'], capture_output=True, text=True)

    assert EXPECTED_OUTPUT == result.stdout