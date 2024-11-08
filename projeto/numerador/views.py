from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import Logar,Novo_registro
from .models import Usuarios,TipoModelo,Registros,Unidades,Numeradores
from datetime import datetime
from django.contrib.auth import login,authenticate


ano_atual = datetime.now().year

def pagina_login(request):
    """
    Renderiza a página de login e processa o formulário de login.

    Se a requisição for do tipo POST, verifica as credenciais do usuário:
      - Busca o usuário pelo nome informado no formulário.
      - Valida a senha e, se correta, armazena `usuario_id` e `unidade_id` na sessão e redireciona para a página `pagina_numerador`.
      - Caso a senha esteja incorreta ou o usuário não exista, retorna uma mensagem de erro.

    Args:
        request (HttpRequest): A requisição HTTP recebida pelo servidor.

    Returns:
        HttpResponse: Se o método for GET, renderiza o formulário de login (`pagina_login.html`).
                      Se o método for POST, redireciona para `pagina_numerador` ou retorna uma mensagem de erro.        
    """
    logar = Logar
    if request.method == "POST":
        logar = Logar(request.POST)
        if logar.is_valid():
            nome_usuario = logar.data['usuario']
            senha = logar.data['senha']
            try:
                usuario = Usuarios.objects.get(nome=nome_usuario)
                if senha == usuario.senha:
                    request.session['usuario_id'] = usuario.id_usuario
                    request.session['unidade_id'] = usuario.unidade_id
                    return redirect('pagina_numerador')
                else:
                    return HttpResponse('Senha Incorreta')
            except Usuarios.DoesNotExist:
                return HttpResponse('Usuario Não encontrado')
            
        
        
    return render(request,'pagina_login.html',{'forms':logar})

def pagina_numerador(request):
    """
    Exibe a página de contadores por modelo para a unidade do usuário logado.

    - Se o usuário não está autenticado, redireciona para `pagina_login`.
    - Obtém todos os modelos e seus contadores (numeradores) específicos para a unidade do usuário.
    - Renderiza a página com o dicionário `numeradores_por_modelo`, que associa cada modelo ao seu contador, junto com o ano atual.

    Args:
        request (HttpRequest): A requisição HTTP recebida pelo servidor.

    Returns:
        HttpResponse: Renderiza `numerador.html` com as informações dos modelos, ano atual e contadores.
    """
    if request.user.is_autenticated:
        unidade_do_usuario = request.session['unidade_id']
        id_do_usuario = request.session['usuario_id']
        unidade_instance = Unidades.objects.get(id_unidade = unidade_do_usuario)
        usuario_instance = Usuarios.objects.get(id_usuario = id_do_usuario)
        numeradores_banco = Numeradores.objects.filter(unidade_id=unidade_instance,is_activate=True)
        lista_numeradores = []
        for numerador_banco in numeradores_banco:
            numerador = {}
            numerador['modelo'] = TipoModelo.objects.get(id_modelo = numerador_banco.modelo_id)
            numerador['contagem'] = numerador_banco.contagem
            
            lista_numeradores.append(numerador)

        
        return render(request,'numerador.html',{'unidade':unidade_instance,'usuario':usuario_instance,'ano':ano_atual,'numeradores':lista_numeradores})
            
    return redirect('pagina_login')
    

def registro(request,id):
    """
    Cria um novo registro associado a um modelo e unidade específicos, e atualiza o numerador.

    - Para requisições POST:
      - Processa o formulário `Novo_registro`, cria uma instância de `Registros` e incrementa o contador de ocorrências do modelo na unidade.
      - Renderiza `novo_registro_criado.html` com detalhes do registro criado.
    - Para requisições GET, exibe o formulário de criação de registro.

    Args:
        request (HttpRequest): A requisição HTTP recebida pelo servidor.
        id (int): Identificador do modelo selecionado.

    Returns:
        HttpResponse: Renderiza `novo_registro_criado.html` para POST ou `novo_registro.html` para GET.
    """
    forms = Novo_registro()
    id_modelo = request.session['modelo_id'] = id
    id_usuario = request.session['usuario_id']
    unidade = request.session['unidade_id']    
    if request.method == "POST":
        forms = Novo_registro(request.POST)
        unidade_istance = Unidades.objects.get(id_unidade=unidade)
        modelo_instance = TipoModelo.objects.get(id_modelo=id_modelo)
        usuario_instance = Usuarios.objects.get(id_usuario=id_usuario)
        data = datetime.now().date()
        titulo = forms.data['titulo']
        observaçao = forms.data['observaçao']
        novo_registro = Registros(titulo=titulo,observacao=observaçao,unidade=unidade_istance,modelo=modelo_instance,
                                  data=data,usuario=usuario_instance)
        if novo_registro:
            try:
                numerador = Numeradores.objects.get(unidade=unidade_istance,modelo=modelo_instance)
                if numerador:
                    numerador.contagem += 1
                    numerador.save()
            except Numeradores.DoesNotExist:
                numerador = Numeradores.criar_numerador(unidade=unidade_istance,modelo=modelo_instance)
            if numerador:
                novo_registro.numeraçao = numerador.contagem
                novo_registro.save()
            else:
                novo_registro.numeraçao = 1
                novo_registro.save()
            return render(request,'novo_registro_criado.html',{'titulo':titulo,'observaçao':observaçao, 'modelo':modelo_instance,'unidade':unidade_istance,'usuario':usuario_instance,'data':data,'numeraçao':novo_registro.numeraçao})     
    return render(request,'novo_registro.html',{'forms':forms,'modelo':id_modelo})      

def listagem(request,id):
    """
    Exibe a lista dos registros recentes para um modelo e unidade específicos.

    - Filtra os registros de `Registros` pelo `modelo_id` e `unidade_id`, ordenados pelos mais recentes.
    - Substitui os IDs de modelo, unidade e usuário pelos nomes correspondentes.
    - Renderiza `lista_registros.html` com os registros.

    Args:
        request (HttpRequest): A requisição HTTP recebida pelo servidor.
        id (int): Identificador do modelo para a listagem.

    Returns:
        HttpResponse: Renderiza `lista_registros.html` com a lista dos registros filtrados.
    """
    modelo_id = request.session['modelo_id'] = id
    unidade = request.session['unidade_id']
    registros = Registros.objects.filter(modelo=modelo_id,unidade=unidade).order_by('-id_registro')[:5]
    for registro in registros:
        modelo_instance = TipoModelo.objects.get(id_modelo=registro.modelo_id)
        registro.modelo_id = modelo_instance.modelo
        unidade_instance = Unidades.objects.get(id_unidade=registro.unidade_id)
        registro.unidade_id = unidade_instance.unidade
        usuario_instance = Usuarios.objects.get(id_usuario=registro.usuario_id)
        registro.usuario_id = usuario_instance.nome
    return render(request,'lista_registros.html',{'lista':registros})   