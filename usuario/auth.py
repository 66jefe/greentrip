from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import AuthenticationFailed, APIException

User = get_user_model()

class Authentication:

    def signin(self, email=None, password=None):
        if not email or not password:
            raise AuthenticationFailed("Email e senha são obrigatórios")

        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed("Email e/ou senha incorretos")

        return user
    
    def signup(self, nome, email, password, telefone, endereco, cidade):
        if not nome:
            raise APIException("O nome não deve ser nulo")

        if not email:
            raise APIException("O email não deve ser nulo")

        if not password:
            raise APIException("A senha não deve ser nula")
        
        if not telefone:
            raise APIException("O telefone é obrigatório")
        if not endereco:
            raise APIException("O endereço é obrigatório")
        if not cidade:
            raise APIException("A cidade é obrigatória")

        if User.objects.filter(email=email).exists():
            raise APIException("Este email já existe")

        user = User.objects.create_user(
            nome=nome,
            email=email,
            telefone=telefone,
            endereco=endereco,
            cidade=cidade,
            password=password
        )

        return user
