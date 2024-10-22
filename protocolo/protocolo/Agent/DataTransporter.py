from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
import hashlib
import sys

def sha256(file_path):
    """Calcula o hash SHA-256 de um arquivo."""
    hash_obj = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

class AgentDataTransporter(Protocol):
    def __init__(self):
        super().__init__()
        self.audioBuffer = b''
        try:
            self.audioFile = sys.argv[1]
        except IndexError:
            print("Faltando argumento")
            self.audioFile = "ERROR"

    def connectionMade(self):
        if self.audioFile != "ERROR":
            try:
                with open(self.audioFile, "rb") as file:
                    self.audioBuffer = file.read()
                    self.transport.write(self.audioBuffer + b'\nEND\n')
                    
                hash_value = sha256(self.audioFile)
                self.transport.write(b'HASH:' + hash_value.encode() + b'\n')
                print(f"Hash enviado: {hash_value}")
            except Exception as error:
                print(f"Erro ao enviar o arquivo: {error}")

        reactor.callLater(1, self.transport.loseConnection)  # Garantir que a transmissão termine

    def connectionLost(self, reason):
        print("Conexão encerrada.")
        reactor.stop()

class AgentTransporterFactory(ClientFactory):
    def buildProtocol(self, addr):
        return AgentDataTransporter()

if __name__ == '__main__':
    try:
        endpoint = TCP4ClientEndpoint(reactor, '127.0.0.1', 2009)
        endpoint.connect(AgentTransporterFactory())
        reactor.run()
    except Exception as error:
        print(f"Erro: {error}")
