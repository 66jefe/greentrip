from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=150)
    cidade = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["nome"]

    objects = UsuarioManager()

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'usuario'

class Publicacao(models.Model):
    titulo = models.CharField(max_length=150, default='')
    descricao = models.TextField(default='')
    especificacao_rota = models.CharField(max_length=250, default='')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="publicacoes")

    class Meta:
        db_table = 'publicacao'

class Imagem(models.Model):
    arquivo = models.ImageField(upload_to='publicacoes/')
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE, related_name="imagens")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    is_principal = models.BooleanField(default=False) #definir a imagem principal da publicação
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "anexos_publicacao"

class Avaliacao(models.Model):
    comentario = models.TextField(blank=True, default='')
    avaliacao = models.DecimalField(max_digits=2, decimal_places=1)
    publicacao = models.ForeignKey(Publicacao, on_delete=models.CASCADE, related_name="avaliacoes")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="avaliacoes")

    class Meta:
        db_table = 'avaliacoes'