// script.js

// Aguarda o HTML ser completamente carregado para executar o script
document.addEventListener('DOMContentLoaded', () => {

    // 1. Referências dos elementos HTML
    const emailInput = document.getElementById('email-input');
    const fileInput = document.getElementById('file-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultSection = document.getElementById('result-section');
    const categoryResult = document.getElementById('category-result');
    const responseResult = document.getElementById('response-result');

    /**
     * Atualiza o estado visual do botão para indicar processamento.
     * @param {boolean} isAnalyzing - true para estado de análise, false para estado normal.
     */
    const updateButtonState = (isAnalyzing) => {
        analyzeBtn.disabled = isAnalyzing;
        analyzeBtn.textContent = isAnalyzing ? 'Analisando...' : 'Analisar';
    };
    
    /**
     * Exibe o resultado da análise ou uma mensagem de erro na interface.
     * @param {object} data - O objeto de resposta da API (ou um objeto de erro).
     */
    const displayResult = (data) => {
        resultSection.classList.remove('hidden');

        if (data.erro) {
            categoryResult.textContent = 'Erro';
            responseResult.textContent = `Ocorreu um problema: ${data.erro}`;
            categoryResult.style.color = 'red';
        } else {
            categoryResult.textContent = data.categoria;
            responseResult.textContent = data.resposta_sugerida;
            categoryResult.style.color = '#333'; // Reseta a cor em caso de sucesso
        }
    };

    /**
     * Lógica principal acionada pelo clique do botão "Analisar".
     */
    analyzeBtn.addEventListener('click', () => {
        const file = fileInput.files[0];
        const emailText = emailInput.value.trim();

        // Prioriza o arquivo se ambos forem fornecidos
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            analyzeContent(formData, 'file'); // Envia o objeto FormData
        } else if (emailText) {
            const jsonData = JSON.stringify({ email: emailText });
            analyzeContent(jsonData, 'json'); // Envia a string JSON
        } else {
            alert('Por favor, insira o texto de um e-mail ou selecione um arquivo.');
        }
    });

    /**
     * Função unificada para enviar o conteúdo para o backend.
     * @param {FormData|string} payload - O corpo da requisição (FormData ou JSON).
     * @param {'file'|'json'} type - O tipo de conteúdo sendo enviado.
     */
    const analyzeContent = async (payload, type) => {
        resultSection.classList.add('hidden');
        updateButtonState(true);

        // Configurações da requisição variam com base no tipo de conteúdo
        const requestOptions = {
            method: 'POST',
            body: payload,
        };
        
        // Se for JSON, adiciona o header específico. Se for FormData, o browser adiciona o header correto.
        if (type === 'json') {
            requestOptions.headers = {
                'Content-Type': 'application/json',
            };
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/processar-email', requestOptions);
            const result = await response.json();

            if (!response.ok) {
                displayResult({ erro: result.erro || 'Houve um problema na resposta do servidor.' });
            } else {
                displayResult(result);
            }

        } catch (error) {
            console.error('Erro ao processar a solicitação:', error);
            displayResult({ erro: 'Não foi possível conectar ao servidor. Verifique se o backend está rodando.' });
        } finally {
            updateButtonState(false);
            // Limpa os campos após a análise
            emailInput.value = '';
            fileInput.value = ''; // Limpa a seleção do arquivo
        }
    };
});