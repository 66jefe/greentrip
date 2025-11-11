from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from usuario.models import Publicacao
from usuario.permissions import IsOwner
from usuario.serializers import PublicacaoSerializer

class PublicacaoListView(ListAPIView):
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class PublicacoesDoUsuarioView(ListAPIView):
    serializer_class = PublicacaoSerializer

    def get_queryset(self):
        usuario_id = self.kwargs["usuario_id"]
        return Publicacao.objects.filter(usuario_id=usuario_id)
    
class PublicacaoDetailView(RetrieveAPIView):
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer