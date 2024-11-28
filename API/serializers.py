from rest_framework import serializers
from numerador.models import Tipocrimes,Categorias,Numeradores,Registros


class TipocrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipocrimes
        fields = '__all__'
    
class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = '__all__'
        
class NumeradoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Numeradores
        fields = '__all__'
        
class DataSerializer(serializers.Serializer):
    data = serializers.CharField()
    
class RegistrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registros
        fields = '__all__'