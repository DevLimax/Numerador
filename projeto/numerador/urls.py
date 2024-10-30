from django.urls import path
from .views import pagina_login,pagina_numerador,registro,listagem

urlpatterns = [
    path('', pagina_login, name='pagina_login'),
    path('numerador/', pagina_numerador, name='pagina_numerador'),
    path('modelo/<int:id>', registro, name='registro'),
    path('listagem/<int:id>', listagem, name='listagem')
]
