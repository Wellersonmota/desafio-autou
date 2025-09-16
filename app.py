# app.py
import os
import fitz # Importa a biblioteca PyMuPDF
from flask import Flask, request, jsonify
from flask_cors import CORS
from ia_service import classificar_e_responder

app = Flask(__name__)
CORS(app)

@app.route('/processar-email', methods=['POST'])
def processar_email():
    try:
        # Verifica se é um upload de arquivo (multipart/form-data)
        if 'file' in request.files:
            file = request.files['file']
            filename = file.filename

            if filename.endswith('.pdf'):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                email_content = ""
                for page in doc:
                    email_content += page.get_text()
                doc.close()
            elif filename.endswith('.txt'):
                email_content = file.read().decode('utf-8')
            else:
                return jsonify({'erro': 'Formato de arquivo não suportado.'}), 400

        # Verifica se é um envio de texto (application/json)
        elif request.is_json:
            data = request.get_json()
            email_content = data.get('email', '')

        else:
             return jsonify({'erro': 'Formato de requisição inválido.'}), 400

        if not email_content:
            return jsonify({'erro': 'Conteúdo do e-mail não fornecido.'}), 400

        resultado_ia = classificar_e_responder(email_content)
        return jsonify(resultado_ia)

    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro no servidor: {str(e)}'}), 500

if __name__ == "__main__":
    print("Servidor da API de classificação de e-mails no ar.")
    app.run(debug=True)