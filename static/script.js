// Aguarda o HTML ser completamente carregado para executar o script
document.addEventListener('DOMContentLoaded', () => {

    // 1. Referências dos elementos HTML
    const emailInput = document.getElementById('email-input');
    const fileInput = document.getElementById('file-input'); // Novo elemento
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
            categoryResult.style.color = '#333';
        }
    };

    // 2. Adiciona o ouvinte de evento para o clique no botão
    analyzeBtn.addEventListener('click', async () => {
        const emailText = emailInput.value.trim();
        const file = fileInput.files[0];

        let contentToSend = '';

        if (file) {
            // Se um arquivo for selecionado, lê o conteúdo dele
            const reader = new FileReader();
            reader.onload = (event) => {
                contentToSend = event.target.result;
                if (contentToSend.trim() === '') {
                    alert('O arquivo selecionado está vazio.');
                    return;
                }
                analyzeContent(contentToSend);
            };
            reader.onerror = () => {
                alert('Ocorreu um erro ao ler o arquivo.');
            };
            reader.readAsText(file);
        } else if (emailText !== '') {
            // Se não houver arquivo, usa o texto da textarea
            contentToSend = emailText;
            analyzeContent(contentToSend);
        } else {
            alert('Por favor, insira o texto de um e-mail ou selecione um arquivo .txt.');
            return;
        }
    });

    /**
     * Função auxiliar para enviar o conteúdo para o backend.
     * @param {string} emailContent - O conteúdo do e-mail a ser analisado.
     */
    const analyzeContent = async (emailContent) => {
        resultSection.classList.add('hidden');
        updateButtonState(true);

        try {
            // 3. Faz a requisição ao backend
            const response = await fetch('http://127.0.0.1:5000/processar-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: emailContent }),
            });

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
            fileInput.value = ''; 
        }
    };
});