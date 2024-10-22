import os
import time
import pytest
import signal
import subprocess
import threading

def test_agent_stop_audio_recording():
    process = subprocess.Popen(
            ['audioRecorder', '-i0', '-t3', '-r3', '-orecordings'],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text=True,
            universal_newlines=True,
            bufsize=1
        )

    time.sleep(1)
    os.kill(process.pid, signal.SIGINT)
    time.sleep(4)
    process.poll()

    assert process.returncode is not None