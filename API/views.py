from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from .serializers import TipocrimeSerializer,CategoriasSerializer,NumeradoresSerializer,DataSerializer,RegistrosSerializer
from rest_framework import status,viewsets
from numerador.models import Tipocrimes,Categorias,Numeradores,Registros
from datetime import datetime


class CrimesViewSet(viewsets.ModelViewSet):
    queryset = Tipocrimes.objects.all()
    serializer_class = TipocrimeSerializer
    
class CategoriasViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializer
    
class NumeradoresViewSet(viewsets.ModelViewSet):
    serializer_class = NumeradoresSerializer
    
    def get_queryset(self):
        queryset = Numeradores.objects.all()
        
        id_numerador = self.request.query_params.get('id_numerador', None)
        unidade_id = self.request.query_params.get('unidade_id', None)
        is_activate = self.request.query_params.get('is_activate', None)
        
        if id_numerador is not None:
            queryset = queryset.filter(id_numerador=id_numerador).order_by('-contagem')
        
        if unidade_id is not None:
            queryset = queryset.filter(unidade_id=unidade_id).order_by('-contagem')
            
        if is_activate is not None:
            is_activate = is_activate.lower() == 'true'
            queryset = queryset.filter(is_activate=is_activate).order_by('-contagem')
            
        return queryset
    
class DataAtualView(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def get(self, request):
        data_atual = datetime.now().date()
        data = {'data':data_atual}
        return Response(data)
    
class RegistrosViewSet(viewsets.ModelViewSet):
    queryset = Registros.objects.all()
    serializer_class = RegistrosSerializer