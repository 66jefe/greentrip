from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, generics

from usuario.models import Publicacao, Avaliacao, Imagem, Usuario
from usuario.permissions import IsOwner, IsSelf
from usuario.serializers import PublicacaoSerializer, AvaliacaoSerializer, UsuarioUpdateSerializer, AlterarSenhaSerializer

class PublicacaoListView(ListAPIView):
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer
    permission_classes = [AllowAny]

class PublicacaoDetailView(RetrieveAPIView):
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer
    permission_classes = [AllowAny]

class PublicacaoCreateView(CreateAPIView):
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        imagens = request.FILES.getlist("imagens")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        publicacao = serializer.save(usuario=request.user)

        for img in imagens:
            Imagem.objects.create(
                publicacao=publicacao,
                usuario=request.user,
                arquivo=img
            )

        output = self.get_serializer(publicacao)
        return Response(output.data, status=status.HTTP_201_CREATED)

class PublicacaoUpdateView(UpdateAPIView):
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        novas_imagens = request.FILES.getlist("imagens")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        imagens_remover = serializer.validated_data.get("imagens_remover", [])

        if imagens_remover:
            Imagem.objects.filter(
                id__in=imagens_remover,
                publicacao=instance
            ).delete()

        serializer.save()

        for img in novas_imagens:
            Imagem.objects.create(
                publicacao=instance,
                usuario=request.user,
                arquivo=img
            )

        output = self.get_serializer(instance)
        return Response(output.data)


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

class UsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioUpdateSerializer
    permission_classes = [IsAuthenticated, IsSelf]

class AlterarSenhaView(generics.UpdateAPIView):
    serializer_class = AlterarSenhaSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user