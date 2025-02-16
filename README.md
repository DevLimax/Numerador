Numerador - Registro de Ocorrências

Site: https://numerador.pythonanywhere.com/home/

O Numerador é um sistema desenvolvido para auxiliar policiais no registro de ocorrências, garantindo a integridade e organização dos dados de cada unidade policial. Cada registro é exclusivo por unidade, impedindo o acesso de uma unidade aos registros de outra.

Tecnologias Utilizadas

Linguagem: Python

Framework: Django e Django Rest Framework (DRF)

Banco de Dados: SQLite

Autenticação: Django Authentication

API: RESTful

Funcionalidades

Cadastro de ocorrências com os seguintes campos:

Título

Observação

Unidade

Categoria do crime

Tipo de crime

Usuário que realizou o registro

Gerenciamento de unidades policiais

Controle de acesso por unidade

API para consulta e registro de ocorrências

Instalação

1. Clonar o Repositório

git clone https://github.com/seu-usuario/numerador.git
cd numerador

2. Criar e Ativar um Ambiente Virtual

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

3. Instalar Dependências

pip install -r requirements.txt

4. Configurar o Banco de Dados

python manage.py migrate
python manage.py createsuperuser  # Criar um usuário administrador

5. Iniciar o Servidor

python manage.py runserver

A API estará disponível em: http://127.0.0.1:8000/

Uso da API

Autenticação

A API utiliza autenticação via token. Para obter um token, faça login enviando uma requisição POST para:

POST /api/token/

Corpo da requisição:

{
    "username": "seu_usuario",
    "password": "sua_senha"
}

Criar uma Ocorrência

POST /api/ocorrencias/

Exemplo de corpo:

{
    "titulo": "Furto de Veículo",
    "observacao": "Veículo furtado em estacionamento",
    "unidade": 1,
    "categoria_crime": "Furto",
    "tipo_crime": "Crime contra o Patrimônio",
    "usuario": 1
}

Listar Ocorrências

GET /api/ocorrencias/

Contribuição

Contribuições são bem-vindas! Para contribuir:

Faça um fork do repositório

Crie uma branch para sua funcionalidade (git checkout -b minha-feature)

Commit suas alterações (git commit -m 'Adicionando nova feature')

Envie para o repositório (git push origin minha-feature)

Abra um Pull Request

Licença

Este projeto é licenciado sob a MIT License.

Desenvolvido por João Pedro 🚀

