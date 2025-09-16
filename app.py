from flask import Flask, request, jsonify
from ia_service import analisar_email_com_ia # <--- IMPORTANTE: Importamos nossa nova função
from flask_cors import CORS

# Substitua pela sua chave de API da Hugging Face
HUGGING_FACE_TOKEN = "token"

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Servidor da API de classificação de emails no ar."

@app.route('/processar-email', methods=['POST'])
def processar_email():
    dados = request.get_json()
    texto_email = dados.get('email_text', '')

    if not texto_email:
        return jsonify({"erro": "Nenhum texto de email fornecido."}), 400

    # --- A MÁGICA ACONTECE AQUI ---
    # Trocamos a lógica simulada pela chamada real à nossa função de IA
    resultado = analisar_email_com_ia(texto_email, HUGGING_FACE_TOKEN)
    
    # Se a função de IA retornar um erro, nós o repassamos
    if "erro" in resultado:
        return jsonify(resultado), 500

    # Devolvemos a resposta que veio da IA
    return jsonify(resultado)