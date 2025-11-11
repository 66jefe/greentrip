from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from usuario.auth import Authentication
from usuario.serializers import UsuarioSerializer

class Signup(APIView):
    authentication_classes = []  # não precisa token
    permission_classes = []       # qualquer um pode criar conta

    def post(self, request):
        nome = request.data.get('nome')
        email = request.data.get('email')
        password = request.data.get('password')
        telefone = request.data.get('telefone')
        endereco = request.data.get('endereco')
        cidade = request.data.get('cidade')

        user = Authentication().signup(
            nome=nome,
            email=email,
            password=password,
            telefone=telefone,
            endereco=endereco,
            cidade=cidade
        )

        serializer = UsuarioSerializer(user)

        return Response(
            {"user": serializer.data},
            status=status.HTTP_201_CREATED
        )
