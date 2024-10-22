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

def test_agent_audio_recording_with_3_repetitions():
    result = subprocess.run(['audioRecorder', '-i0', '-t2', '-r3', '-oaudios'], capture_output=True, text=True)
    saida = result.stdout.split("\n")[:-1]

    verify = True        

    for arquivo in saida:        
        if file_is_wav(str(arquivo)) == False:
            verify = False

    assert verify == True

def test_agent_audio_recording_with_float_number_param():
    result = subprocess.run(['audioRecorder', '-i0', '-t3.999999', '-r1', '-oaudios'], capture_output=True, text=True)
    saida = result.stdout.split("\n")[:-1]

    verify = True        

    for arquivo in saida:        
        if file_is_wav(arquivo) == False:
            verify = False

    assert verify

def test_agent_audio_recording_with_time_less_than_1():
    result = subprocess.run(['audioRecorder', '-i0', '-t0.345', '-r5', '-oaudios'], capture_output=True, text=True)
    saida = result.stdout.split("\n")[:-1]

    verify = True        

    for arquivo in saida:        
        if file_is_wav(arquivo) == False:
            verify = False

    assert verify