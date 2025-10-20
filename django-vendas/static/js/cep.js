// CEP lookup functionality
function buscarCep() {
    const cep = document.getElementById('cep').value.replace(/\D/g, '');
    
    if (cep.length !== 8) {
        return;
    }
    
    // Show loading
    const enderecoInput = document.getElementById('endereco');
    enderecoInput.value = 'Buscando...';
    
    // Call backend API
    fetch(`/clientes/buscar-cep/?cep=${cep}`)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                alert('CEP não encontrado!');
                enderecoInput.value = '';
            } else {
                document.getElementById('endereco').value = data.logradouro;
                document.getElementById('bairro').value = data.bairro;
                document.getElementById('cidade').value = data.cidade;
                document.getElementById('estado').value = data.uf;
            }
        })
        .catch(error => {
            console.error('Erro ao buscar CEP:', error);
            enderecoInput.value = '';
            alert('Erro ao buscar CEP. Tente novamente.');
        });
}

// Attach CEP lookup to input field
document.addEventListener('DOMContentLoaded', function() {
    const cepInput = document.getElementById('cep');
    if (cepInput) {
        cepInput.addEventListener('blur', buscarCep);
    }
});
