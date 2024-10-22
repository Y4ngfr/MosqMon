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

def test_agent_file_not_found_error():
    result = subprocess.run(['audioRecorder', '-i0', '-t0.345', '-r5', '-o../ \n'], capture_output=True, text=True)
    saida = result.stdout.split("\n")[:-1]

    verify = True        

    for arquivo in saida:        
        if file_is_wav(arquivo) == False:
            verify = False

    assert not verify

def test_agent_invalid_input_error():
    EXPECTED_OUTPUT = "Opção `-t` não reconhecida\n"
    result = subprocess.run(['audioRecorder', '-i0', '-t'], capture_output=True, text=True)
    
    assert EXPECTED_OUTPUT == result.stdout

def test_agent_missing_params_error():
    EXPECTED_OUTPUT = "Erro: argumento -r ausente\nErro: argumento -o ausente\n"
    result = subprocess.run(['audioRecorder', '-i0', '-t4'], capture_output=True, text=True)

    assert EXPECTED_OUTPUT == result.stdout