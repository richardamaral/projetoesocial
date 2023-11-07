import re
import time
import pyodbc

from selenium import webdriver
from selenium.common import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

import boto3
import pyautogui
from bs4 import BeautifulSoup

#*************************************************************#
#-------------------------------------------------------------#
#AUTOMAÇÃO PARA REALIZAR CONSULTAS NO E-SOCIAL DE ACORDO COM OS
#ERROS RETORNADOS DA PROCEDURE SQL E APÓS AS CONSULTAS INSERIR
#OS DADOS CORRETOS DOS FUNCIONÁRIOS NO SOC FINALIZANDO O SCRIPT
#-------------------------------------------------------------#
#*************************************************************#



while True:

    #DESATIVAR FAILSAFE PARA ELE CONSEGUIR CLICAR LIVREMENTE
    pyautogui.FAILSAFE = False
    #


    s3 = boto3.client('s3')
    APP = "/??????????????/"
    SECRET_KEY = "/??????????????/"

    nome_bucket = "/??????????????/"

    # CONEXÃO COM BANCO DE DADOS
    cn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=/??????????????/;DATABASE=/??????????????/;UID=py_pro;PWD=/??????????????/')
    cncursor = cn.cursor()

    cncursor.execute("GetInconsistenciaESOCIAL")
    # PEGA OS VALORES DE RETORNO DA PROCEDURE GetInconsistenciaESOCIAL pra pegar o código soc de todas empresas
    resultados = cncursor.fetchall()

    for linha in resultados:
        try:
            navegador = webdriver.Chrome()

            urlgov = "https://login.esocial.gov.br/login.aspx"
            navegador.get(urlgov)
            navegador.maximize_window()
            wait = WebDriverWait(navegador, 30)
            pyautogui.click(1118, 374, duration=1)
            pyautogui.click(1011, 691, duration=1)
            pyautogui.click(845,331, duration=1)
            pyautogui.click(845, 331, duration=1)
            time.sleep(2.5)
            wait = WebDriverWait(navegador, 30)
            try:
                alterar_modulo = navegador.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[2]/a')
                alterar_modulo.click()
            except:
                print("problema na var alterar_modulo")
                navegador.close()
                continue
            wait = WebDriverWait(navegador, 30)
            procurar_cnpj = navegador.find_element(By.XPATH, '/html/body/div[3]/div[4]/div/form/div/section/div[1]/div/select/option[3]')
            procurar_cnpj.click()
            pesquisador = navegador.find_element(By.XPATH, '/html/body/div[3]/div[4]/div/form/div/section/div[3]/div[1]/input')
            pesquisador.send_keys(linha[3])
            verificar = navegador.find_element(By.XPATH, '/html/body/div[3]/div[4]/div/form/div/section/div[3]/div[2]/input').click()
            time.sleep(1)
            try:
                modulo_seg = navegador.find_element(By.XPATH, '/html/body/div[3]/div[4]/div/form/div/section/div[7]/div[2]/div[6]').click()
            except:
                print("FOI DETECTADO UM PROBLEMA AO REALIZAR A AUTOMAÇÃO SOB O ESOCIAL COM O CPNJ", linha[3])
                navegador.close()
                continue
            wait = WebDriverWait(navegador, 30)
            time.sleep(2.5)
            trabalhador = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/nav/button').click()
            time.sleep(0.2)
            trabalhadoresmenu = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/nav/div/ul/li[2]').click()
            time.sleep(2.2)
            wait = WebDriverWait(navegador, 30)
            try:
                entrada_cpf = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/div/div/div/input').send_keys(linha[5])
                pyautogui.click(252, 512, duration=1)
                time.sleep(1.8)
                wait = WebDriverWait(navegador, 30)
                try:
                    matricula = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset/div/div[3]/div/div[2]/ul/li[2]/div/p')
                    matricula = matricula.text
                except:
                    print("ocorreu erro na variavel matricula")
                    navegador.close()
                    continue

                matricula = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset/div/div[3]/div/div[2]/ul/li[2]/div/p')
                matricula = matricula.text
                nome = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset/div/div[2]')
                categoria = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset/div/div[3]/div/div[2]/ul/li[4]/div/p')
                categoria = categoria.text
                dataadmissao = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset/div/div[3]/div/div[2]/ul/li[7]/div/p')
                dataadmissao = dataadmissao.text
                data_desligamento = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset/div/div[3]/div/div[2]/ul/li[8]/div/span')

                if data_desligamento.text == "Data de Desligamento":
                    datademissao = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset/div/div[3]/div/div[2]/ul/li[8]/div/p')
                    datademissao = datademissao.text
                else:
                    print("Não foi salvo nada na variável [datademissao], pois não há data de desligamento!")

                situacao = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset/div/div[3]/div/div[2]/ul/li[1]/div/p')

                situacao = situacao.text

                nome_completo = nome.text

                # Use uma expressão regular para extrair apenas as letras (supondo que o nome contenha apenas letras, espaços e pontos)
                nome = re.sub(r'[^a-zA-Z\s]', '', nome_completo)

                # Imprima o nome
                print(nome, matricula, categoria, dataadmissao, situacao)

                try:
                    print(datademissao)
                except:
                    print("")

            except NoSuchElementException:
                print("Elemento não encontrado, realizando outro tipo de automação para conseguir capturar os dados")
                teste = navegador.find_element(By.XPATH, f'//*[@id="{linha[5]}"]')
                teste.click()
                matricula = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/fieldset/div/div[3]/div/div[2]/ul/li[2]/div/p')
                matricula = matricula.text
                nome = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/fieldset/div/div[2]')
                categoria = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/fieldset/div/div[3]/div/div[2]/ul/li[4]/div/p')
                categoria = categoria.text
                dataadmissao = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/fieldset/div/div[3]/div/div[2]/ul/li[7]/div/p')
                dataadmissao = dataadmissao.text
                data_desligamento = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/fieldset/div/div[3]/div/div[2]/ul/li[8]/div/span')

                if data_desligamento.text == "Data de Desligamento":
                    datademissao = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/fieldset/div/div[3]/div/div[2]/ul/li[8]/div/p')
                    datademissao = datademissao.text
                else:
                    print("Não foi salvo nada na variável [datademissao], pois não há data de desligamento!")

                situacao = navegador.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/fieldset/div/div[3]/div/div[2]/ul/li[1]/div/p')

                situacao = situacao.text

                nome_completo = nome.text

                # Use uma expressão regular para extrair apenas as letras (supondo que o nome contenha apenas letras, espaços e pontos)
                nome = re.sub(r'[^a-zA-Z\s]', '', nome_completo)

                # Imprima o nome
                print(categoria)

            time.sleep(2)

            wait = WebDriverWait(navegador, 30)

            navegador.close()

            senha = ('Password2023')
            driver = webdriver.Chrome()

            driver.get("https://sistema.soc.com.br/WebSoc/")
            driver.maximize_window()  # maximizando a janela
            login = driver.find_element(By.XPATH, '//*[@id="usu"]').send_keys("prorba")  # Colocando o usuario no campo user
            senha = driver.find_element(By.XPATH, '//*[@id="senha"]').send_keys(senha)  # Colocando a senha no campo pass
            time.sleep(0.5)
            # Fazendo a declaração de todos os botões do ID
            botao1 = driver.find_element(By.XPATH, '//*[@id="bt_1"]')
            botao2 = driver.find_element(By.XPATH, '//*[@id="bt_2"]')
            botao3 = driver.find_element(By.XPATH, '//*[@id="bt_3"]')
            botao4 = driver.find_element(By.XPATH, '//*[@id="bt_4"]')
            botao5 = driver.find_element(By.XPATH, '//*[@id="bt_5"]')
            botao6 = driver.find_element(By.XPATH, '//*[@id="bt_6"]')
            botao7 = driver.find_element(By.XPATH, '//*[@id="bt_7"]')
            botao8 = driver.find_element(By.XPATH, '//*[@id="bt_8"]')
            botao9 = driver.find_element(By.XPATH, '//*[@id="bt_9"]')
            botao0 = driver.find_element(By.XPATH, '//*[@id="bt_0"]')
            # Fazendo a declaração de todos os botões do ID
            # VERIFICANDO SE O VALOR DO ATRIBUTO CORRESPONDE AO VALOR DO MEU ID: 6266, PROCURANDO POR TODOS BOTÕES
            # QUANDO ELE ACHAR O BOTÃO DO ID DE VALOR 6 ELE CLICA, 2 ELE CLICA, E ASSIM SUCESSIVAMENTE COMO UM SCAN DOS BOTOES

            #estrutura de condição abaixado prolongada por maior espera da verificação do valor do elemento xpath

            if botao1.get_attribute("value") == "6":
                botao1.click()

            else:
                print('')

            if botao2.get_attribute("value") == "6":
                botao2.click()

            else:
                print('')

            if botao3.get_attribute("value") == "6":
                botao3.click()

            else:
                print('')

            if botao4.get_attribute("value") == "6":
                botao4.click()

            else:
                print('')

            if botao5.get_attribute("value") == "6":
                botao5.click()

            else:
                print('')

            if botao6.get_attribute("value") == "6":
                botao6.click()

            else:
                print('')

            if botao7.get_attribute("value") == "6":
                botao7.click()

            else:
                print('')

            if botao8.get_attribute("value") == "6":
                botao8.click()

            else:
                print('')

            if botao9.get_attribute("value") == "6":
                botao9.click()

            else:
                print('')

            if botao0.get_attribute("value") == "6":
                botao0.click()

            else:
                print('')

            # --------------
            # PROXIMO DIIGTO
            # --------------

            if botao1.get_attribute("value") == "6":
                botao1.click()

            else:
                print('')

            if botao2.get_attribute("value") == "6":
                botao2.click()

            else:
                print('')

            if botao3.get_attribute("value") == "6":
                botao3.click()

            else:
                print('')

            if botao4.get_attribute("value") == "6":
                botao4.click()

            else:
                print('')

            if botao5.get_attribute("value") == "6":
                botao5.click()

            else:
                print('')

            if botao6.get_attribute("value") == "6":
                botao6.click()

            else:
                print('')

            if botao7.get_attribute("value") == "6":
                botao7.click()

            else:
                print('')

            if botao8.get_attribute("value") == "6":
                botao8.click()

            else:
                print('')

            if botao9.get_attribute("value") == "6":
                botao9.click()

            else:
                print('')

            if botao0.get_attribute("value") == "6":
                botao0.click()

            else:
                print('')

            # --------------
            # PROXIMO DIIGTO
            # --------------

            if botao1.get_attribute("value") == "6":
                botao1.click()

            else:
                print('')

            if botao2.get_attribute("value") == "6":
                botao2.click()

            else:
                print('')

            if botao3.get_attribute("value") == "6":
                botao3.click()

            else:
                print('')

            if botao4.get_attribute("value") == "6":
                botao4.click()

            else:
                print('')

            if botao5.get_attribute("value") == "6":
                botao5.click()

            else:
                print('')

            if botao6.get_attribute("value") == "6":
                botao6.click()

            else:
                print('')

            if botao7.get_attribute("value") == "6":
                botao7.click()

            else:
                print('')

            if botao8.get_attribute("value") == "6":
                botao8.click()

            else:
                print('')

            if botao9.get_attribute("value") == "6":
                botao9.click()

            else:
                print('')

            if botao0.get_attribute("value") == "6":
                botao0.click()


            else:
                print('')

            # ---------------
            # PROXIMO DIIGTO
            # ---------------

            if botao1.get_attribute("value") == "5":
                botao1.click()


            else:
                print('')

            if botao2.get_attribute("value") == "5":
                botao2.click()


            else:
                print('')

            if botao3.get_attribute("value") == "5":
                botao3.click()

            else:
                print('')

            if botao4.get_attribute("value") == "5":
                botao4.click()

            else:
                print('')

            if botao5.get_attribute("value") == "5":
                botao5.click()

            else:
                print('')

            if botao6.get_attribute("value") == "5":
                botao6.click()

            else:
                print('')

            if botao7.get_attribute("value") == "5":
                botao7.click()

            else:
                print('')

            if botao8.get_attribute("value") == "5":
                botao8.click()

            else:
                print('')

            if botao9.get_attribute("value") == "5":
                botao9.click()

            else:
                print('')

            if botao0.get_attribute("value") == "5":
                botao0.click()

            else:
                print('')

            time.sleep(1.5)
            entrar = driver.find_element(By.XPATH, '//*[@id="bt_entrar"]').click()  # CLICANDO EM ENTRAR

            time.sleep(1.5)
            try:
                wait = WebDriverWait(driver, 10)
                alertasoc = Alert(driver)
                alertasoc.accept()
                print("Alerta OK")
                time.sleep(0.8)
                driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/ul/li[2]/a/img').click()
            except NoAlertPresentException:
                print('Não foi encontrado nenhum alerta!')

            wait = WebDriverWait(driver, 30)
            iframe = driver.find_element(By.XPATH, '//*[@id="socframe"]')  # MUDANDO O FRAME PRA PODER INTERAGIR COM OS ELEMENTOS DESSE FRAME ESPECIFICO DA PAGINA
            driver.switch_to.frame(iframe)
            caixadebusca = driver.find_element(By.XPATH, '/html/body/form[1]/div[4]/div[2]/p/input')
            caixadebusca.send_keys(linha[1])
            lupa = driver.find_element(By.XPATH, '/html/body/form[1]/div[4]/div[2]/p/a[1]/img')
            lupa.click()
            wait = WebDriverWait(navegador, 30)
            time.sleep(2.5)
            clicarempresa = driver.find_element(By.XPATH, '/html/body/form[1]/div[4]/div[2]/div[2]/table/tbody/tr/td[2]/a')
            clicarempresa.click()
            time.sleep(0.4)
            driver.switch_to.default_content()
            campocod = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/input[1]').click()
            campocod = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/input[1]').send_keys(Keys.BACKSPACE)
            campocod = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/input[1]').send_keys(int('232'))
            time.sleep(1.2)
            campocod1 = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/input[2]').click()
            time.sleep(0.2)

            iframe = driver.find_element(By.XPATH, '//*[@id="socframe"]')  # MUDANDO O FRAME PRA PODER INTERAGIR COM OS ELEMENTOS DESSE FRAME ESPECIFICO DA PAGINA
            driver.switch_to.frame(iframe)

            pesquisa_funcionario = driver.find_element(By.XPATH, '/html/body/div[2]/div/form[1]/fieldset/p[1]/input')

            pesquisa_funcionario.send_keys(linha[4])
            ativarcodigo = driver.find_element(By.XPATH, '/html/body/div[2]/div/form[1]/fieldset/p[7]/span[2]/input')
            ativarcodigo.click()

            buscar = driver.find_element(By.XPATH, '/html/body/div[2]/div/form[1]/fieldset/p[1]/a/img')
            buscar.click()
            time.sleep(0.9)
            funcionario_encontrado = driver.find_element(By.XPATH, '/html/body/div[2]/div/form[1]/table/tbody/tr[2]/td[1]/a')
            funcionario_encontrado.click()
            time.sleep(1.6)
            alterar_funcionario = driver.find_element(By.XPATH, '/html/body/age_nao_gravar/div[2]/div/form/age_nao_gravar/div[1]/table/tbody/tr/td[2]/a[3]/img')
            alterar_funcionario.click()
            time.sleep(1.5)
            wait = WebDriverWait(driver, 30)
            campo_matricula = driver.find_element(By.XPATH, "//input[@name='matriculaFuncionario']")

            campo_matricula.clear()

            campo_matricula.send_keys(matricula)

            # Remova as barras "/" da data
            data_sem_barras = dataadmissao.replace("/", "")

            # Crie uma lista com cada dígito da data
            digitos = list(data_sem_barras)
            dataadmissaosoc = driver.find_element(By.XPATH, "//input[@name='dataAdmissao']")
            dataadmissaosoc.clear()
            # Agora você pode usar cada elemento da lista em suas automações
            for digito in digitos:
                dataadmissaosoc.send_keys(digito)
                time.sleep(0.2)

            time.sleep(0.2)

            if situacao == "Desligado":
                select_element = driver.find_element(By.XPATH, "//select[@id='situacao']")
                dropdown = Select(select_element)
                dropdown.select_by_value('Inativo')
            elif situacao == "Ativo":
                select_element = driver.find_element(By.XPATH, "//select[@id='situacao']")
                dropdown = Select(select_element)
                dropdown.select_by_value('Ativo')
            elif situacao == "Afastado":
                select_element = driver.find_element(By.XPATH, "//select[@id='situacao']")
                dropdown = Select(select_element)
                dropdown.select_by_value('Afastado')
            elif situacao == "Férias":
                select_element = driver.find_element(By.XPATH, "//select[@id='situacao']")
                dropdown = Select(select_element)
                dropdown.select_by_value('Férias')
            else:
                print("Situação não condiz com nenhuma das alternativas disponíveis no SOC")

            wait = WebDriverWait(navegador, 30)
            try:
                data_sem_barras1 = datademissao.replace("/", "")

                # Crie uma lista com cada dígito da data
                digitos1 = list(data_sem_barras1)
                datademissaosoc = driver.find_element(By.XPATH, "//input[@name='dataDemissao ']")
                datademissaosoc.clear()
                for digito1 in digitos1:
                    datademissaosoc.send_keys(digito1)
                    time.sleep(0.2)
            except:
                print("Nenhuma data de desligamento foi preenchida")

            time.sleep(0.2)
            categoriaesocial = driver.find_element(By.XPATH, "//img[@id='iconeAbrirFiltroCategoria']").click()

            time.sleep(2.1)

            if categoria == "Empregado - Geral, inclusive o empregado público da administração direta ou indireta contratado pela CLT" or "101 - Empregado - Geral, inclusive o empregado público da administração direta ou indireta contratado pela CLT":
                pyautogui.click(649, 385, duration=1)  # clicar na opçao 1

            elif categoria == "103 - Jovem Aprendiz":
                pesquisar_categoria = driver.find_element(By.XPATH, "//input[@id='inputFiltroCategoria']")
                pesquisar_categoria.send_keys("103")
                pyautogui.click(430, 350, duration=1)  # clicar no empregado aprendiz - 103

            # elif categoria == "901 - Estagiário":
            #    pesquisar_categoria = driver.find_element(By.XPATH, "//input[@id='inputFiltroCategoria']")
            #    pesquisar_categoria.send_keys("901")
            #    pyautogui.click(465,515, duration=1)  # clicar no empregado aprendiz - 103

            # FUNÇÃO CORREÇÃO DE ESTAGIÁRIOS ACIMA DESABILITADA, POIS A BASE QUE ESTAVA OPERANDO NÃO HAVIA ESTAGIÁRIO.
            else:
                print('O empregado não é CLT')
                pyautogui.click(1034, 214, duration=1)  # clicar no x
            wait = WebDriverWait(navegador, 30)
            time.sleep(0.6)
            gravar = driver.find_element(By.XPATH, "//img[@tooltype='Gravar']")
            gravar.click()
            wait = WebDriverWait(navegador, 30)
            time.sleep(1.5)
            cncursor.execute("Exec DeleteInconsistenciaESOCIAL @InconsistenciaESOCIALId = ?", (linha[0]))
            # ENVIA OS CODIGOS DO CLIENTE PARA SALVAR NA TABELA InconsistenciaESOCIALID, UTILIZANDO A PROCEDURE DeleteInconsistenciaESOCIAL
            cn.commit()
            driver.close()
            print("TERMINANDO LOOP")
        except:
            print("executando bloco except")
            time.sleep(1)
            driver.close()
            print("ocorreu algo de errado com o problema")



