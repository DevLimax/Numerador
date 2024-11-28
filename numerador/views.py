from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from .forms import CadastroForm,LoginForm,RegistroForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Usuarios,Unidades,Categorias,Numeradores,Registros
from django.core.paginator import Paginator
import requests


def cadastro_view(request):
    novo_cadastro = CadastroForm
    
    if request.method == "POST":
        novo_cadastro = CadastroForm(request.POST)
        
        if novo_cadastro:
            username = novo_cadastro["username"].value()
            email = novo_cadastro["email"].value()
            password = novo_cadastro["password"].value()
            password_check = novo_cadastro["confirm_password"].value()
            unidade = novo_cadastro["unidade"].value()
            
            if password != password_check:
                return HttpResponse(f"Senhas não se condizem!{password.value()},{password_check.value()}")
            
            else:
                check_user = User.objects.filter(username=username)
                if check_user:
                    return HttpResponse(f"Ja existe um Usuario com o username:{username}")
                
                create_user_auth = User.objects.create_user(username=username,email=email,password=password)
                create_user_auth.save()
                
                create_user_data = Usuarios.objects.create(auth_uid_id=create_user_auth.id,unidade_id=unidade)
                create_user_data.save()
                return redirect('cadastro_feito')   
            
            
    else:
        return render(request,"CadastroTemplate.html",{"form":novo_cadastro})
    
def cadastro_feito(redirect):
    return render(redirect, 'CadastroFeito.html')

    
    
def login_view(request):
    login_request = LoginForm
    
    if request.method == "POST":
        login_request = LoginForm(request.POST)
        username = login_request["username"].value()
        password = login_request["password"].value()
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            dados_usuario = Usuarios.objects.get(auth_uid_id=user.id)
            request.session['id_usuario'] = user.id
            request.session['unidade_id'] = dados_usuario.unidade_id
            return redirect('home')
        else:
            messages.error(request, "Usuario ou Senha Inválidos")           
            
    return render(request,"LoginTemplate.html",{"form":login_request})

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    if request.user.is_authenticated:
        unidade_usuario = request.session["unidade_id"]
        url_api = "http://127.0.0.1:8000/api/Numeradores/"
        params = {
            'unidade_id':unidade_usuario,
            'is_activate':True
        }
        response  = requests.get(url_api, params=params)
        
        if response.status_code == 200:
            numeradores = response.json()
            for numerador in numeradores:
                numerador['categoria'] = Categorias.objects.get(id_categoria=numerador['categoria'])
            paginator = Paginator(numeradores, 4 )
            page_number = request.GET.get('page')
            paginator_obj = paginator.get_page(page_number)
            return render(request,'HomeTemplate.html',{'page':paginator_obj})
        
        else:
            return HttpResponse(f'Error:{response.status_code}')    
    
    return redirect('login')

def novo_registro_view(request,id_categoria):
    registro = RegistroForm(id_categoria=id_categoria)
    
    if request.method == "POST":
        registro = RegistroForm(request.POST,id_categoria=id_categoria)
        
        if registro:
            url = 'http://127.0.0.1:8000/api/DataAtual/get/'
            data_response = requests.get(url).json()
            titulo = registro['titulo'].value()
            observaçao = registro['observaçao'].value()
            tipo_crime = registro['tipo_do_crime'].value()
            categoria = id_categoria
            usuario = request.session['id_usuario']
            unidade = request.session['unidade_id']
            
            numerador = Numeradores.objects.get(unidade=unidade,categoria=categoria)
            if numerador:
                numerador.contagem += 1
                numerador.save()
                
                url = 'http://127.0.0.1:8000/api/Registros/'
                dados = {
                "data": data_response['data'],
                "titulo": titulo,
                "observacao": observaçao,
                "numeraçao": numerador.contagem,
                "unidade": unidade,
                "categoria": categoria,
                "tipo_crime": int(tipo_crime),
                "usuario": usuario
                }
                
                print(dados)
                response = requests.post(url,json=dados)
                
                if response.status_code == 201:
                    dados_obj = Registros.objects.get(numeraçao=dados['numeraçao'],unidade_id=unidade,categoria_id=categoria,usuario_id=usuario)
                    return render(request, 'RegistroCriado.html',{'dados':dados_obj})
                else:
                    return HttpResponse(f'Error:{response.status_code}')
                
                
                

    return render(request,'NovoRegistroTemplate.html',{'form':registro})
    
def list_numeradores(request,id):
    categoria = Categorias.objects.get(id_categoria=id)
    unidade = request.session['unidade_id']
    registros = Registros.objects.filter(categoria=categoria,unidade=unidade).order_by('-id_registro')[:5]
    
        
    return render(request,'ListaRegistros.html',{'lista':registros})

