# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from ia_service import classificar_e_responder # <-- Note a nova função

app = Flask(__name__)
CORS(app)

@app.route('/processar-email', methods=['POST'])
def processar_email():
    try:
        data = request.get_json()
        email_content = data.get('email', '')
        
        if not email_content:
            return jsonify({'erro': 'Conteúdo do e-mail não fornecido.'}), 400

        # Chama a nova função do serviço de IA
        resultado_ia = classificar_e_responder(email_content)

        # Retorna o resultado completo da IA para o frontend
        return jsonify(resultado_ia)

    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro no servidor: {str(e)}'}), 500

if __name__ == "__main__":
    print("Servidor da API de classificação de e-mails no ar.")
    app.run(debug=True)