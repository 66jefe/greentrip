from rest_framework import serializers
from django.db import models
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Publicacao, Imagem, Avaliacao

class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = [
            "id", 
            "arquivo", 
            "data_criacao"
        ]
        read_only_fields = ["id"]

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
    imagens = ImagemSerializer(many=True, read_only=True)
    imagem_principal = serializers.ImageField(write_only=True, required=False)
    imagens_upload = serializers.ListField(child=serializers.ImageField(),write_only=True,required=False)
    avaliacoes = AvaliacaoSerializer(many=True, read_only=True)
    imagens_remover = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    media = serializers.SerializerMethodField()

    class Meta:
        model = Publicacao
        fields = [
            "id",
            "titulo",
            "descricao",
            "latitude",
            "longitude",
            "endereco",
            "data_criacao",
            "data_atualizacao",
            "imagens",
            "imagem_principal",
            "imagens_upload",
            "avaliacoes",
            "media",
        ]

    def get_media(self, obj):
        qs = obj.avaliacoes.all()
        if qs.exists():
            return qs.aggregate(models.Avg("avaliacao"))['avaliacao__avg']
        return 0

class UsuarioSerializer(serializers.ModelSerializer):
    publicacoes = PublicacaoSerializer(many=True, read_only=True)

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

class UsuarioUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'first_name', 
            'last_name', 
            'email'
        ]

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Este e-mail já está em uso.")
        return value

class AlterarSenhaSerializer(serializers.Serializer):
    senha_atual = serializers.CharField(write_only=True)
    nova_senha = serializers.CharField(write_only=True)
    confirmar_nova_senha = serializers.CharField(write_only=True)

    def validate(self, data):
        usuario = self.context["request"].user

        if not check_password(data["senha_atual"], usuario.password):
            raise serializers.ValidationError({"senha_atual": "Senha atual incorreta."})

        if data["nova_senha"] != data["confirmar_nova_senha"]:
            raise serializers.ValidationError({"nova_senha": "As senhas não coincidem."})

        validate_password(data["nova_senha"], usuario)

        return data

    def save(self, **kwargs):
        usuario = self.context["request"].user
        usuario.set_password(self.validated_data["nova_senha"])
        usuario.save()
        return usuario