# ⚙️🔎 AUTOMAÇÃO PARA CONSULTA E CORREÇÃO DE DADOS DO ESOCIAL NO SISTEMA SOC 🔎⚙️
![Python Version](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![Selenium Version](https://img.shields.io/badge/Selenium-3.141%2B-brightgreen)
![PyAutoGUI Version](https://img.shields.io/badge/PyAutoGUI-0.9%2B-brightgreen)
![PyODBC Version](https://img.shields.io/badge/PyODBC-4.0.39%2B-brightgreen)

Este projeto oferece uma solução automatizada para o processo de manter sincronia dos dados cadastrais dentro do SOC que foram coletados no eSocial.
## Funcionalidades


- **INTEGRAÇÃO COM BANCO DE DADOS**: Ao iniciar o código ele tenta conexão com um banco de dados S3 para retornar em uma lista, dados de funcionários que precisam ser parametrizados dentro do sistema SOC.

- **AUTENTICAÇÃO eSocial**: Utilizando o (Selenium e PyAutoGUI), insiro um certificado digital no navegador para conseguir realizar consultas no eSocial com os dados retornados da procedure com o banco de dados.

- **AUTENTICAÇÃO SOC**: Após consultar as informações necessárias dentro do eSocial e salvar os dados em variáveis, ele realiza a autenticação no sistema SOC.

- **SINCRONIZANDO DADOS**: Estando autenticado e na interface do SOC, executo uma busca pelo colaborador que foi consultado no eSocial para edição e inserção das informações coletadas anteriormente vindas do eSocial.

- **INTEGRAÇÃO COM BANCO DE DADOS**: Após efetuar a correção e confirmação das informações do cadastro corrigido, executo uma linha de código aonde ele irá jogar para outra lista no S3 o ID na lista do colaborador que já foi corrigido, para não ficar repetindo as mesmas correções.

## Como Usar

1. **Configuração do Ambiente**:
   - Certifique-se de ter Python 3.8+ instalado.
   - Instale as bibliotecas necessárias com `pip install selenium pyautogui pyodbc boto3`.
   - Informe uma chave AWS que retorne uma lista de informações que precisam ser corrigidas.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, propor melhorias ou enviar pull requests.

## Autor

- Richard Borges do Amaral