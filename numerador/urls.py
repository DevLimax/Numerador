from django.urls import path
from .views import home_view,cadastro_view,login_view,logout_view,novo_registro_view,cadastro_feito,list_numeradores
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', login_view, name="login"),
    path('cadastro/', cadastro_view, name="Cadastro"),
    path('home/', home_view, name="home"),
    path('logout/', logout_view, name="logout"),
    path('registro/<int:id_categoria>', novo_registro_view, name="novo_registro"),
    path('cadastro_feito/', cadastro_feito, name="cadastro_feito"),
    path('lista_numeradores/<int:id>', list_numeradores, name='lista')
    
]
        