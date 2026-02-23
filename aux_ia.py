import json 
from google import genai
from google.genai import types


class FallBack:
    def __init__(self, api_key):
        self.client_ia = genai.Client(api_key=api_key)
        self.model_ia = "gemini-3-flash-preview"
        
    def encontrar_novo_xpath(self, html_parcial, descricao_elemento):
        prompt = f"""
        CONTEXTO:
        Você é um especialista em automação com Selenium. O XPath atual falhou.
        
        TAREFA:
        Analise o trecho de HTML fornecido abaixo e encontre o XPath para o elemento: '{descricao_elemento}'.
        
        HTML PARA ANÁLISE:
        {html_parcial}
        
        PROCESSO DE PENSAMENTO (THINKING):
        1. Localize todos os elementos que correspondem à descrição.
        2. Identifique se existem duplicatas (elementos com mesmos atributos).
        3. Ignore elementos que pareçam estar escondidos (ex: dentro de áreas invisíveis ou com atributos de ocultação).
        4. Se houver mais de um, use índices como '(//tag[@attr="val"])[2]' para garantir o clique no correto.
        5. Priorize XPaths robustos, mas específicos o suficiente para evitar ambiguidade.

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