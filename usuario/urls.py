from django.urls import path
from usuario.views.visualizacao import PublicacaoListView, PublicacoesDoUsuarioView, PublicacaoDetailView
from usuario.views.signin import Signin
from usuario.views.signup import Signup

urlpatterns = [
    path("publicacoes/", PublicacaoListView.as_view(), name="publicacoes-list"),
    path("usuarios/<int:usuario_id>/publicacoes/", PublicacoesDoUsuarioView.as_view()),
    path("publicacoes/<int:pk>/", PublicacaoDetailView.as_view()),
    path("signin/", Signin.as_view()),
    path("signup/", Signup.as_view()),
]
