from django.urls import  path,include
from .views import CrimesViewSet,CategoriasViewSet,NumeradoresViewSet,DataAtualView,RegistrosViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'TiposCrimes', CrimesViewSet, basename='crimes')
router.register(r'Categorias', CategoriasViewSet, basename='categorias')
router.register(r'Numeradores', NumeradoresViewSet, basename='numeradores')
router.register(r'DataAtual', DataAtualView, basename='DataAtual')
router.register(r'Registros', RegistrosViewSet, basename='registros')

urlpatterns = [
    path('', include(router.urls)),
]
