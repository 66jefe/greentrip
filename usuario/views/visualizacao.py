from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from usuario.models import Publicacao, Avaliacao
from usuario.permissions import IsOwner
from usuario.serializers import PublicacaoSerializer, AvaliacaoSerializer

"""
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
    serializer_class = PublicacaoSerializer"""

class PublicacaoListView(ListAPIView):
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer
    parmission_classes = [AllowAny]

class PublicacaoDetailView(RetrieveAPIView):
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer
    permission_classes = [AllowAny]

class PublicacaoCreateView(CreateAPIView):
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class PublicacaoUpdateView(UpdateAPIView):
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class PublicacaoDeleteView(DestroyAPIView):
    queryset = Publicacao.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

class PublicacoesDoUsuarioView(ListAPIView):
    serializer_class = PublicacaoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        usuario_id = self.kwargs["usuario_id"]
        return Publicacao.objects.filter(usuario_id=usuario_id)

class AvaliacoesDaPublicacaoView(ListAPIView):
    serializer_class = AvaliacaoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        publicacao_id = self.kwargs["publicacao_id"]
        return Avaliacao.objects.filter(publicacao_id=publicacao_id)

class AvaliacaoCreateView(CreateAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        publicacao_id = self.kwargs["publicacao_id"]
        serializer.save(
            usuario=self.request.user,
            publicacao_id=publicacao_id
        )

class AvaliacaoUpdateView(UpdateAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class AvaliacaoDeleteView(DestroyAPIView):
    queryset = Avaliacao.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]