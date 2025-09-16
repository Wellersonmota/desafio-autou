# Importa a função que queremos testar
from ia_service import analisar_email_com_ia

# --- CONFIGURAÇÃO DO TESTE ---
# Cole seu token da Hugging Face aqui
MEU_TOKEN = "token" 

# Texto de e-mail que queremos analisar
EMAIL_EXEMPLO = "Olá, gostaria de saber o status do meu pedido 456. Obrigado."
# --- FIM DA CONFIGURAÇÃO ---


# Executa a função e imprime o resultado
if __name__ == "__main__":
    if MEU_TOKEN == "SEU_TOKEN_AQUI":
        print("!!! ATENÇÃO: Por favor, substitua 'SEU_TOKEN_AQUI' pelo seu token real no arquivo teste_ia.py")
    else:
        resultado = analisar_email_com_ia(EMAIL_EXEMPLO, MEU_TOKEN)
        print("\n--- RESULTADO DO TESTE ---")
        print(resultado)
        print("--- FIM DO TESTE ---\n")