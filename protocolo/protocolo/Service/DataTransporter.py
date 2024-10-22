from twisted.internet import reactor, protocol
from twisted.internet.protocol import Protocol, ServerFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
import hashlib
import sys

def sha256(data):
    """Calcula o hash SHA-256 dos dados recebidos."""
    hash_obj = hashlib.sha256()
    hash_obj.update(data)
    return hash_obj.hexdigest()

class ServiceDataTransporter(Protocol):
    def __init__(self):
        super().__init__()
        self.data = b''
        self.expected_hash = None
        try:
            self.audioFile = sys.argv[1]
        except Exception as error:
            print("Faltando argumento nome do arquivo")
            self.audioFile = "ERROR"

    def dataReceived(self, data):
        if b'\nEND\n' in data:
            # Separar o conteúdo do arquivo do restante
            parts = data.split(b'\nEND\n')
            self.data += parts[0]  # Conteúdo do arquivo

            if len(parts) > 1 and parts[1].startswith(b'HASH:'):
                self.expected_hash = parts[1][5:].strip().decode()  # Extrair o hash
                self.check_integrity()
        else:
            self.data += data

    def check_integrity(self):
        # Calcular o hash do conteúdo recebido
        received_hash = sha256(self.data)
        # print(f"Hash calculado: {received_hash}")
        # print(f"Hash esperado: {self.expected_hash}")

        if received_hash == self.expected_hash:
            self.transport.write(b'Integridade verificada com sucesso!\n')
            print("\nIntegridade verificada com sucesso!\n")
            self.save_file()
        else:
            self.transport.write(b'Falha na integridade do arquivo!\n')
            print("\nFalha na integridade do arquivo!\n")

    def save_file(self):
        try:
            with open(self.audioFile, "wb") as file:
                file.write(self.data)
            print("\nArquivo salvo com sucesso\n")
        except Exception as error:
            print(f"Erro ao salvar o arquivo: {error}")

    def connectionLost(self, reason):
        reactor.stop()

class ServiceTransporterFactory(ServerFactory):
    def buildProtocol(self, addr):
        return ServiceDataTransporter()

if __name__ == '__main__':
    try:
        transferEndpoint = TCP4ServerEndpoint(reactor, 2009)
        transferEndpoint.listen(ServiceTransporterFactory())
        reactor.run()
    except Exception as error:
        print(f"Erro: {error}")
