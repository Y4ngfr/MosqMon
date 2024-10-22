NEGRITO="\e[1m"
RESET="\e[0m"
VERDE="\e[32m"
VERMELHO="\e[31m"
AMARELO="\e[33m"
AZUL="\e[34m"

escrever_no_meio() {
    local mensagem="$1"
    local largura_terminal=$(tput cols)
    local cor="$2"
    local comprimento_msg=${#mensagem}
    local margem_esquerda=$(( (largura_terminal - comprimento_msg) / 2 ))
    printf "%*s${cor}${NEGRITO}%s${RESET}\n" "$margem_esquerda" "" "$mensagem"
}

# pytest -v --tb=short --durations=0 testes/testes_RF01.py.

escrever_no_meio "RF01 -- Iniciar Gravação" "$VERMELHO"
pytest -v tests/system_tests_RF01.py tests/agent_tests_RF01.py

escrever_no_meio "RF02 -- Interromper Gravação" "$VERMELHO"
pytest -v tests/system_tests_RF02.py tests/agent_tests_RF02.py

escrever_no_meio "RF03 -- Obter Faixa de Áudio" "$VERMELHO"
pytest -v tests/system_tests_RF03.py

escrever_no_meio "RF04 -- Obter Situação do Agente" "$VERMELHO"
pytest -v tests/system_tests_RF04.py

escrever_no_meio "RF05 -- Listar Faixas de Áudio" "$VERMELHO"
pytest -v tests/system_tests_RF05.py

escrever_no_meio "RF06 -- Apagar Faixa de Áudio" "$VERMELHO"
pytest -v tests/system_tests_RF06.py

escrever_no_meio "RF07 -- Renomear Arquivo de Áudio" "$VERMELHO"
pytest -v tests/system_tests_RF07.py

escrever_no_meio "RF -- Validar Entrada do Usuário" "$VERMELHO"
pytest -v tests/system_input_validation.py tests/agent_input_validation.py