# ia_service.py
from transformers import pipeline

# Pipeline 1: Classificação de texto (existente e otimizado)
# Este modelo classifica a emoção, que usamos para definir a categoria.
classificador = pipeline(
    "text-classification", 
    model="bhadresh-savani/distilbert-base-uncased-emotion",
    truncation=True
)

# Pipeline 2: Geração de texto para respostas dinâmicas (novo)
# Este modelo irá gerar uma resposta com base em um prompt.
gerador_resposta = pipeline(
    "text-generation",
    model="distilgpt2"
)

def classificar_e_responder(email_content):
    try:
        # --- ETAPA DE CLASSIFICAÇÃO (Inalterada) ---
        resultado_classificacao = classificador(email_content)[0]
        label_emocao = resultado_classificacao['label']
        
        if label_emocao in ['surprise', 'fear', 'sadness', 'anger']:
            categoria = 'Produtivo'
            # Prompt para a IA generativa focado em ação e resolução
            prompt = "Em resposta a um e-mail importante sobre um problema, a resposta profissional começa com: 'Prezado(a), recebemos sua mensagem e estamos tratando do assunto. Priorizaremos sua solicitação e"
        else:
            categoria = 'Improdutivo'
            # Prompt para a IA generativa focado em agradecimento
            prompt = "Em resposta a um e-mail informativo, a resposta cordial começa com: 'Prezado(a), agradecemos pelo seu contato e pela informação compartilhada. Manteremos"

        # --- ETAPA DE GERAÇÃO DE RESPOSTA COM IA (Novo) ---
        # Geramos uma resposta curta e coesa usando o prompt definido.
        # max_length controla o tamanho da resposta para ser concisa.
        # num_return_sequences=1 garante apenas uma sugestão.
        resposta_gerada_lista = gerador_resposta(prompt, max_length=50, num_return_sequences=1)
        resposta_sugerida = resposta_gerada_lista[0]['generated_text']

        return {"categoria": categoria, "resposta_sugerida": resposta_sugerida}

    except Exception as e:
        print(f"Erro ao processar o e-mail com a IA: {e}")
        return {"categoria": "Erro", "resposta_sugerida": f"Ocorreu um erro ao processar o e-mail: {str(e)}"}