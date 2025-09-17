# Desafio AutoU: Analisador de E-mails com IA

## Descrição do Projeto

Esta é uma aplicação web desenvolvida como parte do desafio técnico da AutoU. A solução utiliza inteligência artificial para analisar o conteúdo de e-mails, classificar o sentimento predominante (ex: alegria, tristeza, raiva) e, com base nessa análise, gerar uma sugestão de resposta. O objetivo é otimizar o tempo e a eficiência na comunicação, fornecendo um rascunho de resposta contextualizado.

A interface permite que o usuário insira o texto do e-mail de duas formas: colando o texto diretamente em uma área de input ou fazendo o upload de arquivos nos formatos `.txt` e `.pdf`.

## Tecnologias Utilizadas

* **Backend:**
    * Python 3
    * Flask (para a criação da API REST)
    * Hugging Face Transformers (para os modelos de IA)
    * PyMuPDF (para extração de texto de arquivos PDF)
* **Frontend:**
    * HTML5
    * CSS3
    * JavaScript (puro, para requisições assíncronas via `fetch`)
* **Modelos de IA:**
    * `distilbert-base-uncased-emotion`: Utilizado para a classificação de sentimentos.
    * `distilgpt2`: Utilizado para a geração de texto (sugestão de resposta).

## Como Executar Localmente

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

**1. Clone o Repositório**
```bash
git clone [URL_DO_SEU_REPOSITORIO_AQUI]
cd [NOME_DO_SEU_REPOSITORIO]
```

**2. Crie e Ative um Ambiente Virtual**
*No Windows:*
```bash
python -m venv venv
venv\Scripts\activate
```
*No macOS/Linux:*
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as Dependências**
Certifique-se de que o ambiente virtual está ativado e execute o comando:
```bash
pip install -r requirements.txt
```

**4. Execute a Aplicação**
```bash
python app.py
```

**5. Acesse no Navegador**
Abra seu navegador e acesse a seguinte URL:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---
