import json 
from google import genai
from google.genai import types


class FallBack:
    def __init__(self, api_key):
        self.client_ia = genai.Client(api_key=api_key)
        self.model_ia = "gemini-3-flash-preview"
        # self.modo="thinking" ligar o thinking aumenta token mas deixa mais esperto
        
    def encontrar_novo_xpath(self, html_parcial, descricao_elemento, url, titulo, acao):
        prompt = f"""
        CONTEXTO:
        Você é um especialista em automação com Selenium. O XPath atual falhou.

        INFORMAÇÕES DA PÁGINA:
        URL: {url}
        TÍTULO: {titulo}
        TIPO DE AÇÃO: {acao}

        TAREFA:
        Analise o HTML abaixo e encontre o XPath mais robusto para o elemento:
        '{descricao_elemento}'.

        Considere que a ação a ser executada é: {acao}.
        O XPath deve priorizar elementos visíveis e interativos.

        HTML PARA ANÁLISE:
        {html_parcial}

        REGRAS:
        1. Evite XPaths frágeis baseados em índices absolutos.
        2. Priorize atributos estáveis como id, name, aria-label, texto visível.
        3. Se houver duplicidade, utilize índice apenas se necessário.
        4. Considere o contexto da URL e título para entender a finalidade da página.

        RESPOSTA OBRIGATÓRIA EM JSON:
        {{
            "novo_xpath": "string",
            "analise_de_duplicatas": "string",
            "motivo": "string"
        }}
        """
        
        try:
            response = self.client_ia.models.generate_content(
                model=self.model_ia,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                    system_instruction="Você é um especialista em Selenium e XPath. Sua missão é salvar a automação."
                )
            )
            return json.loads(response.text)
        except Exception as e:
            return {"Erro": str(e)}