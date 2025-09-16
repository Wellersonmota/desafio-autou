# ia_service.py
from transformers import pipeline

# Ao carregar o pipeline, adicionamos o parâmetro 'truncation=True'.
# Isso instrui o classificador a cortar automaticamente qualquer texto
# que exceda o comprimento máximo de entrada do modelo (512 tokens).
classificador = pipeline(
    "text-classification", 
    model="bhadresh-savani/distilbert-base-uncased-emotion",
    truncation=True
)

def classificar_e_responder(email_content):
    try:
        # A chamada da função permanece a mesma. A lógica de truncagem é
        # agora gerenciada de forma transparente pelo pipeline.
        resultado_local = classificador(email_content)[0]
        
        # A lógica de mapeamento baseada nas emoções permanece inalterada.
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