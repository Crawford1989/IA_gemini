🤖 Selenium Self-Healing with Gemini AI
🚀 A Ideia do Projeto
Automações de interface (UI) são famosas por serem "frágeis". Uma pequena mudança no layout de um site ou uma atualização de classes CSS pode quebrar um script de horas.

Este projeto introduz uma camada de Autocura (Self-Healing). Quando o Selenium falha ao encontrar um elemento (como um botão ou campo de busca), 
em vez de encerrar o processo com um erro, o script invoca a inteligência artificial do Gemini (Google AI Studio). 
A IA analisa o HTML em tempo real, identifica o novo local do elemento e atualiza automaticamente as configurações do robô.

🧠 Como Funciona?
Tentativa Padrão: O robô lê o XPath de um arquivo config.json e tenta interagir com a página.

Gatilho de Falha: Se ocorrer um NoSuchElementException ou ElementNotInteractableException, a classe FallBack é acionada.

Análise da IA: Enviamos um "snapshot" do HTML parcial para o modelo Gemini 1.5 Flash.

Raciocínio (Chain of Thought): A IA identifica duplicatas, ignora elementos ocultos e gera um novo XPath resiliente.

Persistência: O novo XPath é testado. Se funcionar, o arquivo config.json é sobrescrito, evitando que o erro ocorra na próxima execução.

🛠️ Tecnologias Utilizadas
Python 3.12: Base do projeto.

Selenium & Undetected Chromedriver: Para navegação e contorno de detecção de bots.

Google Generative AI (Gemini API): O "cérebro" responsável pela análise e recuperação de elementos.

Pandas: (Opcional) Para manipulação de dados extraídos.

📋 Pré-requisitos
Python 3.12+

Uma chave de API do Google AI Studio.

Variáveis de ambiente configuradas no arquivo .env.

🔧 Instalação e Uso
Clone o repositório:

Bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
Crie e ative seu ambiente virtual:

Bash
python -m venv venv_ia
# Windows:
.\venv_ia\Scripts\activate
Instale as dependências:

Bash
pip install -r requirements.txt
Configure suas chaves:
Crie um arquivo .env na raiz e adicione:

Snippet de código
GEMINI_API_KEY=SuaChaveAqui
Execute o Robô:

Bash
python robo.py

📈 Diferenciais deste Projeto
Redução de Manutenção: Menos intervenção humana para ajustes simples de UI.

Inteligência de Visibilidade: Diferente de outras soluções, este projeto valida se o elemento está visível antes de sugerir o novo caminho.

Configuração Dinâmica: Uso de JSON para gerenciar seletores de forma externa ao código.

📄 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.
