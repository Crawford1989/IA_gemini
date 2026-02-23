from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import undetected_chromedriver as uc
from aux_ia import FallBack  
import time
from dotenv import load_dotenv
import os
import json
load_dotenv()

def gerenciar_config(acao, chave, valor=None):
    arquivo = 'config.json'
    with open(arquivo, 'r') as f:
        dados = json.load(f)
        
    if acao == 'ler':
        return dados.get(chave)
    elif acao == 'salvar':
        dados[chave] = valor
        with open(arquivo, 'w') as f:
            json.dump(dados, f, indent=4)
            print(f"💾 Novo XPath salvo no JSON para a chave '{chave}'!")
            
            

def iniciar_robo():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    
    # Certifique-se que o nome da classe no outro arquivo é exatamente FallBack
    verificador = FallBack(api_key=os.getenv("GEMINI_API_KEY")) 
    
    try:
        driver.get("https://www.google.com")
        time.sleep(2)
        
        id_elemento = "botao_sorte"
        xpath_atual = gerenciar_config('ler', id_elemento)
        print(f"🔍 Usando XPath do JSON: {xpath_atual}")
        
        try:
            # AJUSTE AQUI: Em vez de find_element, usamos find_elements para filtrar o visível
            elementos = driver.find_elements("xpath", xpath_atual)
            clicou_sucesso = False
            
            for el in elementos:
                if el.is_displayed() and el.is_enabled():
                    el.click()
                    print("✅ Sucesso ao clicar no botão de primeira!")
                    clicou_sucesso = True
                    break
            
            # Se achou o elemento mas nenhum era clicável, força o erro para ir ao Fallback
            if not clicou_sucesso:
                raise NoSuchElementException("Elemento existe mas não está visível")
        
        except (NoSuchElementException, ElementNotInteractableException):
            print("\n🚨 O XPath do JSON falhou! Iniciando Autocura...")
            
            # Pega o HTML para a IA analisar
            html_snapshot = driver.page_source[:20000]
            resultado = verificador.encontrar_novo_xpath(html_snapshot, "Botão 'Estou com sorte'")
            
            if "novo_xpath" in resultado:
                novo_xpath = resultado["novo_xpath"]
                print(f"🤖 IA sugeriu: {novo_xpath}")
                
                # Procura todos os elementos que batem com a sugestão da IA
                elementos = driver.find_elements("xpath", novo_xpath)
                clicou = False
                
                for el in elementos:
                    # O pulo do gato: verifica se o botão está realmente na tela
                    if el.is_displayed(): 
                        try:
                            el.click()
                            # SÓ SALVAMOS SE O CLIQUE FUNCIONAR
                            gerenciar_config('salvar', id_elemento, novo_xpath)
                            print(f"🔥 Robô curado! Novo XPath salvo: {novo_xpath}")
                            clicou = True
                            break
                        except Exception as e:
                            print(f"⚠️ Tentativa de clique falhou: {e}")
                
                if not clicou:
                    print("❌ A IA até achou um caminho, mas nenhum elemento estava clicável no momento.")
            else:
                print("❌ A IA não conseguiu identificar um novo caminho no HTML fornecido.")
                
    finally:
        print("🏁 Finalizando driver...")
        try:
            driver.quit() 
        except:
            pass


if __name__ == '__main__':
    iniciar_robo()