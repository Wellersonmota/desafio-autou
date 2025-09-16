# ia_service.py
import requests
from transformers import pipeline

# Novo modelo para classificação de emoções
# Instale este modelo no seu terminal:
# pip install torch torchvision torchaudio sentencepiece

# Mude a URL para o modelo de emoções
classificador = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

def classificar_e_responder(email_content):
    try:
        resultado_local = classificador(email_content)[0]
        
        # A nova lógica de mapeamento se baseia nas emoções
        # 'surprise' ou 'fear' indicam algo inesperado ou um problema, logo, Produtivo
        # 'joy' ou 'sadness' indicam que o e-mail não necessita de uma ação, logo, Improdutivo
        categoria_analisada = resultado_local['label']
        
        if categoria_analisada in ['surprise', 'fear', 'sadness']:
            categoria = 'Produtivo'
            resposta_sugerida = 'Obrigado pelo seu e-mail! Vamos seguir com a sua solicitação.'
        else:
            categoria = 'Improdutivo'
            resposta_sugerida = 'Obrigado pela sua mensagem. Sua informação foi recebida.'

        return {"categoria": categoria, "resposta_sugerida": resposta_sugerida}

    except Exception as e:
        print(f"Erro ao processar o e-mail localmente: {e}")
        return {"categoria": "Erro", "resposta_sugerida": "Ocorreu um erro ao processar o e-mail."}