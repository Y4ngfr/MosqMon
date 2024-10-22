from twisted.internet import reactor, endpoints, ssl
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.endpoints import SSL4ClientEndpoint
from twisted.internet.ssl import optionsForClientTLS
from twisted.python import log
import sys
import subprocess
import threading
import os
import signal

class AgentControllerProtocol(Protocol):
    def __init__(self):
        super().__init__()
        self.header = ""        #
        self.requestType = ""   #
        self.response = "ok"      # status do data transporter
        self.transporterThread = threading.Thread(target=self.runDataTransporter)
        self.transporterProcess: bytes
        self.recorderThread = threading.Thread(target=self.recordAudio)
        self.recorderArgumentsField: list[str]
        self.fileName = ""
        self.recorderPID = -1

    def parseRequest(self, request:bytes):
        self.header = request.decode('utf-8')
        self.requestType = (self.header.split('\n')[1]).split()[1]

    def actOnRequest(self):
        if self.requestType == "START_MONITORING":
            self.recorderArgumentsField = (self.header.split('\n')[1]).split()[2:]
            if self.recorderPID == -1:
                self.recorderThread.start()
                self.transport.write(b"REPLY - Monitoring Protocol\nType: START_MONITORING\nRecording audio")
            else:
                self.transport.write(b"REPLY - Monitoring Protocol\nType: START_MONITORING\nRequest not allowed")
        
        if self.requestType == "PULL_AUDIO":
            try:
                nameArray = self.header.split('\n')[2].split()[1:]
                self.fileName = nameArray[0]
                nameArray.pop(0)
                for fileName in nameArray:
                    self.fileName += " " + fileName
                try:
                    fileNumber = int(self.fileName)
                    self.fileName = os.listdir("audios")[fileNumber]
                except:
                    pass
            except:
                self.fileName = ""
            reply = "REPLY - Monitoring Protocol\nType: PULL_AUDIO\nFile: " + self.fileName
            self.transport.write(bytes(reply, 'utf-8'))

        if self.requestType == "DATA_TRANSFER":
            self.transporterThread.start()
            self.transport.write(b"REPLY - Monitoring Protocol\nType: DATA_TRANSFER\nStart")

        if self.requestType == "LIST":
            audioList = os.listdir("audios")
            messageReply = "REPLY - Monitoring Protocol\nType: LIST\n"
            for audio in audioList:
                messageReply += audio + "\n"
            self.transport.write(bytes(messageReply, 'utf-8'))

        if self.requestType == "DELETE":
            file = (self.header.split('\n')[2])
            try:
                fileNumber = int(file)
                fileIsANumber = True
            except:
                fileIsANumber = False
                file = (self.header.split('\n')[2]).split('\"')[1]

            messageReply = "REPLY - Monitoring Protocol\nType: DELETE\n"

            try:
                if fileIsANumber:
                    audioList = os.listdir("audios")
                    os.remove(f"audios/{audioList[fileNumber]}")
                    messageReply += "file deleted: " + audioList[fileNumber]
                    self.transport.write(bytes(messageReply, 'utf-8'))
                else:
                    os.remove(f"audios/{file}")
                    messageReply += "file deleted: " + file
                    self.transport.write(bytes(messageReply, 'utf-8'))
            except Exception as error:
                # qualquer erro
                messageReply += str(error)
                self.transport.write(bytes(messageReply, 'utf-8'))

        if self.requestType == "RENAME":
            filesField = (self.header.split('\n')[2])
            currentName = ""
            newName = ""
            messageReply = "REPLY - Monitoring Protocol\nType: RENAME\n"
            try:
                if filesField[0] == '\"':
                    # arquivo é uma string
                    currentName = filesField.split('\"')[1]
                    newName = filesField.split('\"')[3]
                    os.rename(f"audios/{currentName}", f"audios/{newName}")
                    messageReply += "File " + currentName + "renamed to: " + newName
                else:
                    # arquivo é um número
                    numberFile = int(filesField.split()[0])
                    newName = filesField.split('\"')[1]
                    audioList = os.listdir("audios")
                    os.rename(f"audios/{audioList[numberFile]}", f"audios/{newName}")
                    messageReply += f"File {audioList[numberFile]} renamed to: {newName}"
                self.transport.write(bytes(messageReply, 'utf-8'))
            except Exception as error:
                messageReply += str(error)
                self.transport.write(bytes(messageReply, 'utf-8'))

        if self.requestType == "STOP_MONITORING":
            if self.recorderPID != -1:
                os.kill(self.recorderPID, signal.SIGINT)
                self.recorderThread.join()
                self.recorderPID = -1
                self.transport.write(b"REPLY - Monitoring Protocol\nType: STOP_MONITORING\nSuccessfully stopped")
            else:
                self.transport.write(b"REPLY - Monitoring Protocol\nType: STOP_MONITORING\nWas not running")
        
        if self.requestType == "CLOSE_CONNECTION":
            print("Fechando Conexão...")
            if self.recorderPID != -1:
                os.kill(self.recorderPID, signal.SIGINT)
                self.recorderThread.join()
            self.transport.loseConnection()

        if self.requestType == "STATUS":
            reply = ""
            if self.recorderPID == -1:
                reply = "REPLY - Monitoring Protocol\nType: STATUS\nAudio Recorder: audio is ready\n"
            else:
                reply = "REPLY - Monitoring Protocol\nType: STATUS\nAudio Recorder: recording audio...\n"

            reply += "Data Transporter: " + self.response
            self.transport.write(bytes(reply, 'utf-8'))

        if self.requestType == "DEVICES":
            process = subprocess.run(['audioRecorder', '--devices'], capture_output=True, text=True)
            reply = "REQUEST - Monitoring Protocol\nType: DEVICES\nDevices: "
            reply += process.stdout
            self.transport.write(bytes(reply, 'utf-8'))

    def runDataTransporter(self):
        try:
            self.transporterProcess = subprocess.run(['python3', 'Agent/DataTransporter.py', f"audios/{self.fileName}"], capture_output=True, text=True)
            self.transporterThread = threading.Thread(target=self.runDataTransporter)
            self.response = self.transporterProcess.stdout
        except Exception as error:
            print(error)
        
    def recordAudio(self):
        deviceIndex = "-i" + self.recorderArgumentsField[0]
        recordingTime = "-t" + self.recorderArgumentsField[1]
        recordingLoops = "-r" + self.recorderArgumentsField[2]
        output = "-o" + "audios"

        process = subprocess.Popen(
            ['audioRecorder', deviceIndex, recordingTime, recordingLoops, output],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text=True,
            universal_newlines=True,
            bufsize=1
        )
        self.recorderPID = process.pid
        process.wait()
        for line in process.stdout:
            print(line, end='')
        self.recorderPID = -1
        # saída do processo é stdout e erros é stderr
        # return_code é process.returncode
        # subprocess.run(['audioRecorder', deviceIndex, recordingTime, recordingLoops, output])
        self.recorderThread = threading.Thread(target=self.recordAudio)

    def connectionMade(self):
        self.transport.write(b"REPLY - Monitoring Protocol\nType: READY_TO_START")
        
    def dataReceived(self, request):
        self.parseRequest(request)
        self.actOnRequest()

    def connectionLost(self, reason):
        reactor.stop()

class AgentControllerFactory(ClientFactory):
    def buildProtocol(self, addr):
        return AgentControllerProtocol()
    
if __name__ == '__main__':
    try:
        reactor.connectSSL('localhost', 2008, AgentControllerFactory(), ssl.ClientContextFactory())
        # controllerEndpoint = TCP4ClientEndpoint(reactor, '127.0.0.1', 2008)
        # controllerEndpoint.connect(AgentControllerFactory())
        reactor.run()
    except Exception as error:
        print(error)