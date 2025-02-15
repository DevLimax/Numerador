document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const categories = document.querySelectorAll('.category-container');

    searchInput.addEventListener('input', function () {
        const filter = searchInput.value.toLowerCase(); // Obtém o valor da pesquisa em minúsculo

        categories.forEach(category => {
            const title = category.querySelector('.crime-title').textContent.toLowerCase(); // Título em minúsculo
            if (title.includes(filter)) {
                category.style.display = 'block'; // Mostra o container correspondente
            } else {
                category.style.display = 'none'; // Esconde os não correspondentes
            }
        });
    });
});

// Menu de opções (exemplo)
document.addEventListener('DOMContentLoaded', function () {
    const menuButton = document.getElementById('menuButton');

    menuButton.addEventListener('click', function () {
        alert('Funcionalidade do menu pode ser implementada aqui!');
    });
});