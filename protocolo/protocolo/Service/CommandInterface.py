import cmd

# implementar um comando para listar os dispositivos de áudio

class CommandInterface(cmd.Cmd):
    prompt = 'Interface do Serviço> '

    def __init__(self):
        super().__init__() # Deve-se iniciar a classe mãe (Cmd)
        self.msg = None
        # self.sendDataAllowed = False

    def do_START_MONITORING(self, line):
        """ 
        Executa o gravador de acordo com os parâmetros fornecidos. Os áudios são salvos automaticamente.
        Uso: START_MONITORING <deviceIndex> <recordingTime> <recordingLoops>.
        deviceIndex: índice do dispositivo de gravação de áudio (Use DEVICES).
        recordingTime: tempo de gravação do áudio (número real).
        recordingLoops: quantidade de áudios gravados repetidamente (número inteiro).
        """
        try:
            arguments = line.split()
            if len(arguments) != 3:
                print("Erro: forneça 3 parâmetros")
                return
            
            deviceIndex = int(arguments[0])
            recordingTime = float(arguments[1])
            recordingLoops = int(arguments[2])

        except ValueError:
            print("Erro: forneça parâmetros válidos (consulte a ajuda)")
            return

        self.msg = "REQUEST - Monitoring Protocol\nType: START_MONITORING "
        self.msg += line

        return True

    def do_STOP_MONITORING(self, line):
        """
        Verifica se há alguma gravação corrente e interrompe o gravador.
        Não requer argumentos.
        """
        self.msg = "REQUEST - Monitoring Protocol\nType: STOP_MONITORING"
        return True

    def do_STATUS(self, line):
        """
        Imprime o estado do gravador e do processo de transporte de áudio.
        Não requer argumentos.
        """
        self.msg = "REQUEST - Monitoring Protocol\nType: STATUS"
        return True

    def do_PULL_AUDIO(self, line):
        """
        Faz o download do audio selecionado.
        Uso: PULL_AUDIO <arquivo de audio>.
        É possível usar tanto o nome do arquivo com extensão wav quanto o seu índice na lista de áudios (use LIST).
        """
        if len(line.split()) < 1:
            print("Erro: forneça o número do arquivo ou o seu nome entre aspas")
            return
        try:
            # Arquivo é um número
            int(line)
        except:
            # Arquivo é uma string
            if line[0] != '\"' or line[len(line) - 1] != '\"':
                print("Erro: nome do arquivo deve estar entre aspas")
                return
        file = line.replace('"', "")
        self.msg = "REQUEST - Monitoring Protocol\nType: PULL_AUDIO\n" + "File: " + file
        return True
        
    def do_CLOSE_CONNECTION(self, line):
        """
        Verifica se há algum processo em andamento e encerra a conexão.
        Não requer argumentos.
        """
        self.msg = "REQUEST - Monitoring Protocol\nType: CLOSE_CONNECTION"
        return True
    
    def do_LIST(self, line):
        """
        Lista todos os arquivos de áudio gravados.
        Não requer argumentos.
        """
        self.msg = "REQUEST - Monitoring Protocol\nType: LIST"
        return True
    
    def do_DELETE(self, line):
        """
        Deleta o arquivo de áudio selecionado.
        Uso: DELETE <arquivo de áudio>.
        É possível usar tanto o nome do arquivo com extensão wav quanto o seu índice na lista de áudios (use LIST).
        """
        if len(line.split()) < 1:
            print("Erro: forneça o número do arquivo ou o seu nome entre aspas")
            return
        
        try:
            # Arquivo é um número
            int(line)
        except:
            # Arquivo é uma string
            if line[0] != '\"' or line[len(line) - 1] != '\"':
                print("Erro: nome do arquivo deve estar entre aspas")
                return

        file = line
        self.msg = "REQUEST - Monitoring Protocol\nType: DELETE\n" + file
        return True
    
    def do_RENAME(self, line):
        """
        Renomeia um arquivo de áudio.
        Uso: RENAME <arquivo de áudio> <novo nome>
        É possível usar tanto o nome do arquivo com extensão wav quanto o seu índice na lista de áudios (use LIST).
        """
        if len(line.split()) < 2:
            print("Erro: forneça o número do arquivo ou o seu nome entre aspas e o novo nome entre aspas")
            return
        fileIsANumber: bool
        try:
            int(line.split()[0])
            fileIsANumber = True
        except:
            fileIsANumber = False

        if fileIsANumber:
            nameArray = line.split()[1:]
            newName = ""
            for name in nameArray:
                newName += name + " "
            # ultimo caractere de newName é um espaço

            if newName[0] != '\"' or newName[len(newName) - 2] != '\"':
                print("Erro: novo nome do arquivo deve estar entre aspas")
                return
        else:
            try:
                currentName = line.split('\"')[1]
                newName = line.split('\"')[3]

                if line[0] != '\"' or line[len(currentName) + 1] != '\"':
                    print("Erro: nome do arquivo deve estar entre aspas")
                    return
                if len(line) - 3 - len(newName) != len(currentName) + 2:
                    print("Erro: sintaxe inválida (consulte a ajuda)")
                    return
                if line[len(line) - 1] != '\"' or  line[len(line) - 2 - len(newName)] != '\"':
                    print("Erro: novo nome do arquivo deve estar entre aspas")
                    return
            except:
                print("Erro: os nomes de arquivo devem estar entre aspas")
                return
            
        self.msg = "REQUEST - Monitoring Protocol\nType: RENAME\n" + line
        return True
    
    def do_DEVICES(self, line):
        """
        Lista os dispositivos de áudio disponíveis.
        Não requer argumentos.
        """
        self.msg = "REQUEST - Monitoring Protocol\nType: DEVICES"
        return True
        
if __name__ == '__main__':
    interface = CommandInterface()
    interface.cmdloop()