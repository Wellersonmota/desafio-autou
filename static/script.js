// Aguarda o HTML ser completamente carregado para executar o script
document.addEventListener('DOMContentLoaded', () => {

    // 1. Referências dos elementos HTML
    const emailInput = document.getElementById('email-input');
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
        analyzeBtn.textContent = isAnalyzing ? 'Analisando...' : 'Analisar E-mail';
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
            categoryResult.style.color = 'red'; // Feedback visual de erro
        } else {
            categoryResult.textContent = data.categoria;
            responseResult.textContent = data.resposta_sugerida;
            categoryResult.style.color = '#333'; // Volta à cor padrão
        }
    };

    // 2. Adiciona o ouvinte de evento para o clique no botão
    analyzeBtn.addEventListener('click', async () => {
        const emailText = emailInput.value.trim();

        if (emailText === '') {
            alert('Por favor, insira o texto de um e-mail.');
            return;
        }

        // Esconde resultados antigos e atualiza o estado do botão
        resultSection.classList.add('hidden');
        updateButtonState(true);

        try {
            // 3. Faz a requisição ao backend
            const response = await fetch('http://127.0.0.1:5000/processar-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email_text: emailText }),
            });

            const result = await response.json();

            if (!response.ok) {
                // Se a resposta da API não for 200 OK, trata o erro da API
                displayResult({ erro: result.erro || 'Houve um problema na resposta do servidor.' });
            } else {
                // Exibe o resultado de sucesso
                displayResult(result);
            }

        } catch (error) {
            // Trata erros de rede ou de requisição
            console.error('Erro ao processar a solicitação:', error);
            displayResult({ erro: 'Não foi possível conectar ao servidor. Verifique se o backend está rodando.' });
        } finally {
            // Sempre volta o botão ao estado normal no final
            updateButtonState(false);
        }
    });
});