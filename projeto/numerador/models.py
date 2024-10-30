from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import psycopg2

class Unidades(models.Model):
    """
    Modelo representando uma unidade.

    Campos:
        id_unidade (AutoField): Chave primária da unidade.
        unidade (CharField): Nome da unidade.

    Métodos:
        __str__: Retorna o nome da unidade para exibição.
    """
    id_unidade = models.AutoField(primary_key=True)  
    unidade = models.CharField(max_length=200, null=False)

    def str(self):
        return self.unidade
        


class Usuarios(models.Model):
    """
    Modelo representando um usuário.

    Campos:
        id_usuario (AutoField): Chave primária do usuário.
        nome (CharField): Nome do usuário.
        senha (CharField): Senha do usuário (armazenada como hash).
        unidade (ForeignKey): Unidade associada ao usuário (chave estrangeira para o modelo Unidades).

    Métodos:
        __str__: Retorna o nome do usuário para exibição.
    """
    id_usuario = models.AutoField(primary_key=True)  
    nome = models.CharField(max_length=200, null=False)
    senha = models.CharField(max_length=200, null=False)
    unidade = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name='usuarios')  

    def str(self):
        return self.nome


class TipoModelo(models.Model):
    """
    Modelo representando um tipo de modelo.

    Campos:
        id_modelo (AutoField): Chave primária do tipo de modelo.
        modelo (CharField): Nome do tipo de modelo.

    Métodos:
        __str__: Retorna o nome do modelo para exibição.
    """
    id_modelo = models.AutoField(primary_key=True)  
    modelo = models.CharField(max_length=200, null=False)

    def str(self):
        return self.modelo

        


class Registros(models.Model):
    """
    Modelo representando um registro.

    Campos:
        id_registro (AutoField): Chave primária do registro.
        unidade (ForeignKey): Unidade associada ao registro (chave estrangeira para Unidades).
        modelo (ForeignKey): Tipo de modelo associado ao registro (chave estrangeira para TipoModelo).
        data (DateField): Data do registro.
        usuario (ForeignKey): Usuário que criou o registro (chave estrangeira para Usuarios).
        titulo (CharField): Título do registro.
        observacao (CharField): Observação adicional sobre o registro.
        numeracao (IntegerField): Número único do registro para o modelo e unidade.

    Métodos:
        __str__: Retorna o título do registro ou "Registro sem título" se estiver vazio.
    """
    id_registro = models.AutoField(primary_key=True) 
    unidade = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name='registros') 
    modelo = models.ForeignKey(TipoModelo, on_delete=models.CASCADE, related_name='registros')  
    data = models.DateField(null=False)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='registros')  
    titulo = models.CharField(max_length=200, null=True, blank=True)
    observacao = models.CharField(max_length=200, null=True, blank=True)
    numeraçao = models.IntegerField(null=False,default=0)

    def str(self):
        return self.titulo if self.titulo else "Registro sem título"
    
    
class Numeradores(models.Model):
    """
    Modelo representando um numerador (contador) para uma unidade e tipo de modelo.

    Campos:
        id_numerador (AutoField): Chave primária do numerador.
        unidade (ForeignKey): Unidade associada ao numerador (chave estrangeira para Unidades).
        modelo (ForeignKey): Tipo de modelo associado ao numerador (chave estrangeira para TipoModelo).
        contagem (IntegerField): Contador das ocorrências do modelo para a unidade.

    Métodos:
        __str__: Retorna o valor do contador.
        criar_numerador: Cria um novo numerador para uma unidade e modelo com contagem inicial de 1.
    """
    id_numerador = models.AutoField(primary_key=True)
    unidade = models.ForeignKey(Unidades, on_delete=models.CASCADE, related_name='contador')
    modelo = models.ForeignKey(TipoModelo, on_delete=models.CASCADE, related_name='contador')  
    contagem = models.IntegerField(default=0,null=False)
    
    def __str__(self):
        return str(self.contagem)


    def criar_numerador(unidade,modelo):
        numerador = Numeradores(unidade=unidade,modelo=modelo,contagem = 1)
        numerador.save()
        print('Numerador Criado')