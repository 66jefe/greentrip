from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from usuario.auth import Authentication
from usuario.serializers import UsuarioSerializer

class Signin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # valida email/senha e retorna usuário  
        user = Authentication().signin(email=email, password=password)

        # gera tokens JWT
        token = RefreshToken.for_user(user)

        # serializa o usuário
        serializer = UsuarioSerializer(user)

        return Response(
            {
                "user": serializer.data,
                "refresh": str(token),
                "access": str(token.access_token)
            },
            status=status.HTTP_200_OK
        )
