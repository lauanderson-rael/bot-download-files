'''
1 - Entrar no site https://consulta-empresa.netlify.app/
2 - Fazer o login(clicar no campo usuario, digitar usuario, clicar no campo senha, digitar senha, clicar em entrar)
3 - Baixar o PDF de cada empresa e apos isso renomear cada um deles, com o nome da empresa que ele pertence
    - extrair o nome de cada empresa e guarda numa lista[]
    - A cada momento que baixar um arquivo, ele sera renomeado para o nome da sua EMPRESA
4 - Repetir passo 3 até baixar todos PDFs
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import os

# Configuracao Chrome
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    # Não pedir permissão para fazer download
    'download.prompt_for_download': False,
    # Local padrão para armazenar downloads
    'download.default_directory': r'D:\estudos e projetos\Python\automacao01\bot-download-files\relatorios',
    # Não pedir permissão para fazer múltiplos downloads
    'profile.default_content_setting_values.automatic_downloads': 1,
})

# PROCESSO DE LOGIN
try:
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://consulta-empresa.netlify.app/')
    sleep(3)

    campo_usuario = driver.find_element(By.XPATH,"//input[@id='username']")
    campo_senha = driver.find_element(By.XPATH,"//input[@id='password']")
    botao_entrar = driver.find_element(By.XPATH,"//button[@type='submit']")

    # 1 - Preenchendo campos e clicando no botao
    campo_usuario.send_keys('jhonatan');
    sleep(1)
    campo_senha.send_keys('12345678');
    sleep(1)
    botao_entrar.click();
    sleep(4)

    # 2 - Verificando se foi realizado o login
    if "protected" in driver.current_url:
        print('Login realizado com sucesso\n')
    else:
        print("Falha no login. Verifique as credenciais ou o fluxo do site.")
except Exception as e:
    print(f"Erro ao realizar o login: {e}")

# COLETANDO NOMES DAS EMPRESAS

def baixar_relatorios(driver):
    # 1 - Guardar nomes da empresas numa lista
    nomes_empresas = driver.find_elements(By.XPATH, "//td[@name='nome_empresa']"); sleep(2)
    botoes_download_pdf = driver.find_elements(By.XPATH, "//button[@class='download-btn']"); sleep(2)

    # 2 - A cada momento que baixar um arquivo, ele sera renomeado para o nome da sua EMPRESA
    for nome, botao_pdf in zip(nomes_empresas, botoes_download_pdf):
        botao_pdf.click()
        sleep(2)
        # aguardar o download finalizar, pegar o nome do arquivo e renomear para o nome da empresa
        diretorio = r'D:\estudos e projetos\Python\automacao01\bot-download-files\relatorios'
        nome_antigo = 'perfil_empresa.pdf'
        novo_nome = f'{nome.text}.pdf'
        # montando caminho completo para renomear
        caminho_completo_antigo = os.path.join(diretorio, nome_antigo)
        caminho_completo_novo = os.path.join(diretorio, novo_nome)
        #renomear os arquivos
        os.rename(caminho_completo_antigo, caminho_completo_novo)

baixar_relatorios(driver=driver)
botao_prox_pagina = driver.find_element(By.XPATH, "//button[@id='nextBtn']")
while botao_prox_pagina.get_attribute('disabled') == None:
    botao_prox_pagina.click()
    baixar_relatorios(driver=driver)


print("Arquivos baixados e renomeados com sucesso!")

input('Pressione ENTER para sair ')
driver.quit()
