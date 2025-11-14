from rest_framework import serializers
from django.db import models
from .models import Usuario, Publicacao, Imagem, Avaliacao

class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = [
            "id", 
            "arquivo", 
            "data_criacao"
        ]

class AvaliacaoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.nome', read_only=True)

    class Meta:
        model = Avaliacao
        fields = [
            "id",
            "comentario",
            "avaliacao",
            "usuario_nome",
            "usuario",
            "publicacao"
        ]

        read_only_fields = ["usuario", "publicacao"]


class PublicacaoSerializer(serializers.ModelSerializer):
    imagens = ImagemSerializer(source='imagem_set', many=True, read_only=True)
    avaliacoes = AvaliacaoSerializer(source="avaliacao_set", many=True, read_only=True)
    media = serializers.SerializerMethodField()

    class Meta:
        model = Publicacao
        fields = [
            "id",
            "descricao",
            "data_criacao",
            "data_atualizacao",
            "imagens",
            "avaliacoes",
            "media",
        ]

        def get_media(self, obj):
            qs = obj.avaliacao_set.all()

            if qs.exists():
                return qs.aggregate(models.Avg("avalicaco"))['avaliacao__avg']
            return 0

class UsuarioSerializer(serializers.ModelSerializer):
    publicacoes = PublicacaoSerializer(source='publicacao_set', many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "nome",
            "email",
            "telefone",
            "endereco",
            "cidade",
            "publicacoes"
        ]
        read_only_fields = ["id", "data_criacao"]
