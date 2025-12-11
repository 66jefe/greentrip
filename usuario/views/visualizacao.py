from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        publicacao = serializer.save(usuario=request.user)

        output = self.get_serializer(publicacao)
        return Response(output.data, status=status.HTTP_201_CREATED)

class PublicacaoUpdateView(UpdateAPIView):
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        imagem_principal = request.FILES.get("imagem_principal")
        novas_imagens = request.FILES.getlist("imagens_upload")
        imagens_remover = serializer.validated_data.get("imagens_remover", [])

        print("VALIDATED:", serializer.validated_data)

        if not isinstance(imagens_remover, list):
            imagens_remover = []

        serializer.save()

        if imagem_principal:
            Imagem.objects.filter(
                publicacao=instance, is_principal=True
            ).update(is_principal=False)

            Imagem.objects.create(
                publicacao=instance,
                usuario=request.user,
                arquivo=imagem_principal,
                is_principal=True
            )

        for img in novas_imagens:
            Imagem.objects.create(
                publicacao=instance,
                usuario=request.user,
                arquivo=img,
                is_principal=False
            )

        output = self.get_serializer(instance)
        return Response(output.data)

class DefinirPrincipalView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        imagem_id = request.data.get("imagem_id")
        if not imagem_id:
            return Response({"erro": "imagem_id é obrigatório"}, status=400)

        try:
            publicacao = Publicacao.objects.get(pk=pk, usuario=request.user)
        except Publicacao.DoesNotExist:
            return Response({"erro": "Publicação não encontrada"}, status=404)

        try:
            nova_principal = Imagem.objects.get(pk=imagem_id, publicacao=publicacao)
        except Imagem.DoesNotExist:
            return Response({"erro": "Imagem não encontrada"}, status=404)

        # desmarca anterior
        Imagem.objects.filter(publicacao=publicacao, is_principal=True).update(is_principal=False)

        # marca nova
        nova_principal.is_principal = True
        nova_principal.save()

        # retorna lista atualizada
        imagens = Imagem.objects.filter(publicacao=publicacao)
        data = [{
            "id": img.id,
            "arquivo": img.arquivo.url,
            "is_principal": img.is_principal
        } for img in imagens]

        return Response({"imagens": data})


class PublicacaoDeleteView(DestroyAPIView):
    queryset = Publicacao.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

class PublicacoesDoUsuarioView(ListAPIView):
    serializer_class = PublicacaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario_id = self.kwargs["usuario_id"]
        return Publicacao.objects.filter(usuario_id=usuario_id).order_by("-data_criacao")


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
        print(self.request.data)  # Ver o que chega
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