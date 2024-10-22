from twisted.internet import reactor, protocol, endpoints
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.protocol import ServerFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.python.failure import Failure
from twisted.internet.endpoints import SSL4ServerEndpoint
from twisted.internet.ssl import DefaultOpenSSLContextFactory
from twisted.internet.ssl import CertificateOptions
from CommandInterface import CommandInterface
from twisted.python import log
import sys
import subprocess
import threading
import time

# Baseado no tutorial https://www.youtube.com/watch?v=_XGlpzjbbvU&list=PLP6YTIItbLXPxv85Xx8sh8xVk8zMjjcCh
    
class ServiceControllerProtocol(Protocol):
    def __init__(self):
        super().__init__()
        self.header = ""                                                            # 
        self.responseType = ""                                                      # 
        self.request = ""                                                           # Requisição a ser mandada para o agente
        self.transporterThread = threading.Thread(target=self.runDataTransporter)   # Thread do DataTransporter
        self.transporterIsRunning = False
        self.fileName = ""

    def parseResponse(self, response:bytes):
        self.header = response.decode("utf-8")
        self.responseType = (self.header.split('\n')[1]).split()[1]

    def actOnResponse(self):
        if self.responseType == "START_MONITORING":
            print()
            print(self.header.split('\n')[2])
            print()

        if self.responseType == "PULL_AUDIO":
            try:
                nameArray = self.header.split('\n')[2].split()[1:]
                self.fileName = nameArray[0]
                nameArray.pop(0)
                for fileName in nameArray:
                    self.fileName += " " + fileName
            except:
                self.fileName = ""
            self.transporterThread.start()
            time.sleep(1) # espera para ter certeza que o DataTransporter iniciou
            self.transporterIsRunning = True
            
        if self.responseType == "DATA_TRANSFER":
            self.transporterThread.join()
            self.transporterIsRunning = False
            time.sleep(1)

        if self.responseType == "LIST":
            print()
            audioList = self.header.split('\n')[2:]
            i=0
            for audio in audioList:
                print(f"{i} - {audio}")
                i = i + 1
                if i == len(audioList) - 1:
                    break
            print()

        if self.responseType == "DELETE":
            print()
            print(self.header.split('\n')[2])
            print()

        if self.responseType == "RENAME":
            print()
            print(self.header.split('\n')[2])
            print()

        if self.responseType == "STOP_MONITORING":
            print()
            if self.header.split('\n')[2] == "Successfully stopped":
                print("Gravação foi interrompida com sucesso")
            else:
                print("Não estava gravando")
            print()

        if self.responseType == "STATUS":
            print()
            print(self.header.split('\n')[2])
            print(self.header.split('\n')[3])
            print()

        if self.responseType == "DEVICES":
            print()
            devices = self.header.split('\n')[3:]
            devicesStr = ""
            for device in devices:
                devicesStr += device + '\n'
            print("Dispositivos de gravação de áudio:")
            print(devicesStr, end='')

    def runDataTransporter(self):
        try:
            subprocess.run(['python3', 'Service/DataTransporter.py', f"correspondencia/{self.fileName}"])
            self.transporterThread = threading.Thread(target=self.runDataTransporter)
        except Exception as error:
            print(error)

    def sendMessage(self):
        if self.transporterIsRunning == False:
            interface = CommandInterface()
            interface.cmdloop()
            self.request = interface.msg
            self.transport.write(bytes(self.request, 'utf-8'))
        else:
            self.transport.write(b"REQUEST - Monitoring Protocol\nType: DATA_TRANSFER")

    def connectionMade(self):
        print("Bem-vindo! Digite 'help' ou '?' para listar os comandos.\n")

    def dataReceived(self, response):
        self.parseResponse(response)
        self.actOnResponse()
        self.sendMessage()

    def connectionLost(self, reason): 
        print("Conexão encerrada")
        reactor.stop()

class ServiceControllerFactory(ServerFactory):
    def buildProtocol(self, addr):
        return ServiceControllerProtocol()

if __name__ == '__main__':
    try:
        ssl_context = DefaultOpenSSLContextFactory(
            privateKeyFileName='server.key',
            certificateFileName='server.crt'
        )

        options = CertificateOptions()
        print(options.method)

        sslEndpoint = endpoints.SSL4ServerEndpoint(reactor, 2008, ssl_context)
        sslEndpoint.listen(ServiceControllerFactory())
        # controllerEndpoint = TCP4ServerEndpoint(reactor, 2008)
        # controllerEndpoint.listen(ServiceControllerFactory())
        reactor.run()
    except Exception as error:
        print(error)