import requests
import os
import re # Precisamos da lib re para expressão regular

# --- VARIÁVEIS DE CONFIGURAÇÃO ---
# URL da API de inferência da Hugging Face para um modelo de classificação de texto
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

# Token de API do Hugging Face (obtido de variáveis de ambiente)
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

def analisar_email_com_ia(email_text: str, token: str) -> dict:
    """
    Envia o texto de um e-mail para a API da Hugging Face para classificação de sentimento
    e sugere uma resposta baseada nisso.

    Args:
        email_text (str): O conteúdo do e-mail a ser analisado.
        token (str): O token de API para autenticação na Hugging Face.

    Returns:
        dict: Um dicionário contendo a categoria de sentimento e a resposta sugerida,
              ou uma mensagem de erro.
    """
    if not token:
        return {"erro": "Token de API do Hugging Face não configurado."}

    headers = {"Authorization": f"Bearer {token}"}

    # O modelo distilbert-base-uncased-finetuned-sst-2-english espera o texto diretamente
    # para classificar em "POSITIVE" ou "NEGATIVE".
    payload = {
        "inputs": email_text
    }

    print("Enviando para a IA...")
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Levanta um erro para status HTTP ruins (4xx ou 5xx)

        # A API retorna uma lista de listas de dicionários para este tipo de modelo
        ia_response = response.json()
        print(f"Resposta completa do servidor: {ia_response}")

        categoria = "Geral" # Categoria padrão
        resposta_sugerida = "Recebemos sua mensagem e entraremos em contato em breve."

        # --- PARSE DA RESPOSTA DA IA ---
        # Exemplo de resposta para este modelo: [[{'label': 'POSITIVE', 'score': 0.999}, {'label': 'NEGATIVE', 'score': 0.000}]]
        if ia_response and isinstance(ia_response, list) and ia_response[0]:
            scores = ia_response[0]
            # Encontrar a label com a maior pontuação
            best_sentiment = max(scores, key=lambda x: x['score'])

            if best_sentiment['label'] == 'POSITIVE' and best_sentiment['score'] > 0.8:
                categoria = "Positivo"
                resposta_sugerida = "Agradecemos o seu feedback positivo! Estamos felizes em ajudar."
            elif best_sentiment['label'] == 'NEGATIVE' and best_sentiment['score'] > 0.8:
                categoria = "Negativo"
                resposta_sugerida = "Lamentamos qualquer inconveniente. Um de nossos agentes entrará em contato para resolver isso."
            else:
                categoria = "Neutro"
                resposta_sugerida = "Recebemos sua mensagem e entraremos em contato em breve."

        # Para manter a estrutura original de "classificação de e-mail"
        # Precisaríamos de um modelo LLM que gerasse isso.
        # Como estamos com um classificador de sentimento, a categoria será baseada no sentimento.
        # A categoria de "Vendas", "Suporte" etc. exigiria um modelo LLM ou um fine-tuning.
        # Para este modelo, vamos simplificar para "Positivo", "Negativo", "Neutro".

        return {
            "categoria": categoria,
            "resposta_sugerida": resposta_sugerida
        }

    except requests.exceptions.RequestException as e:
        print(f"Erro na chamada da API: {e}")
        return {"erro": f"Falha ao comunicar com a API de IA: {e}"}
    except Exception as e:
        print(f"Erro inesperado no processamento da IA: {e}")
        return {"erro": f"Erro interno ao processar IA: {e}"}

# A função find_pattern não será mais necessária com este modelo,
# mas se o seu app.py ou ia_service.py depender dela, você pode mantê-la
# ou removê-la se não for mais usada.
def find_pattern(text, pattern):
    """
    Função auxiliar para encontrar padrões regex no texto.
    Não é usada com o modelo atual, mas mantida por referência.
    """
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None