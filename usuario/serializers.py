from rest_framework import serializers
from .models import Usuario, Publicacao, Imagem

class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = ["id", "arquivo", "data_criacao"]

class PublicacaoSerializer(serializers.ModelSerializer):
    imagens = ImagemSerializer(source='imagem_set', many=True, read_only=True)

    class Meta:
        model = Publicacao
        fields = [
            "id",
            "descricao",
            "data_criacao",
            "data_atualizacao",
            "imagens",
        ]

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
