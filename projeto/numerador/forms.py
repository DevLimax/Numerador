from django import forms

class Novo_registro(forms.Form):
    """
    Formulário para criar um novo registro.

    Campos:
        titulo (CharField): Campo opcional para o título do registro, com limite de 200 caracteres.
        observacao (CharField): Campo opcional para observações adicionais, com limite de 2000 caracteres.
    """
    titulo = forms.CharField(max_length=200,required=False)
    observaçao = forms.CharField(max_length=2000,required=False)
    
    
class Logar(forms.Form):
    """
    Formulário para autenticação de usuário.

    Campos:
        usuario (CharField): Nome de usuário, obrigatório, com limite de 100 caracteres.
        senha (CharField): Senha do usuário, obrigatória e exibida como campo de senha, com limite de 50 caracteres.
    """
    usuario = forms.CharField(max_length=100)
    senha = forms.CharField(widget=forms.PasswordInput,max_length=50)
    

    