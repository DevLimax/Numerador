from django import forms
from .models import Unidades,Tipocrimes

class CadastroForm(forms.Form):
    username = forms.CharField(max_length=200)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput,max_length=20)
    confirm_password = forms.CharField(widget=forms.PasswordInput,max_length=20)
    unidade = forms.ModelChoiceField(queryset=Unidades.objects.all(),empty_label="Escolha uma unidade")
    
class LoginForm(forms.Form):
    username  = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput,max_length=20)

class RegistroForm(forms.Form):    
    titulo = forms.CharField(max_length=200,required=False)
    observaçao = forms.CharField(max_length=200,required=False)
    tipo_do_crime = forms.ModelChoiceField(queryset=Tipocrimes.objects.none(),empty_label='Selecione o Tipo do crime')     

    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id_categoria', None) 
        super().__init__(*args, **kwargs) 
        if id:
            self.fields['tipo_do_crime'].queryset = Tipocrimes.objects.filter(categoria_crime_id=id)
