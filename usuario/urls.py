from django.urls import path
from usuario.views.visualizacao import *
from usuario.views.signin import Signin
from usuario.views.signup import Signup

urlpatterns = [
    #rotas publicações
    path("publicacoes/", PublicacaoListView.as_view(), name="publicacao-list"),
    path("publicacoes/<int:pk>/", PublicacaoDetailView.as_view(), name="publicacao-detail"),
    path("publicacoes/criar/", PublicacaoCreateView.as_view(), name="publicacao-create"),
    path("publicacoes/<int:pk>/editar/", PublicacaoUpdateView.as_view(), name="publicacao-update"),
    path("publicacoes/<int:pk>/deletar/", PublicacaoDeleteView.as_view(), name="publicacao-delete"),

    #rota publicações dos usuarios
    path("usuario/<int:usuario_id>/publicacoes/", PublicacoesDoUsuarioView.as_view(),  name="publicacoes-do-usuario"),

    #edição do usuario
    path("usuario/<int:pk>/", UsuarioDetailView.as_view(), name="usuario-detail"),
    path("usuario/alterar-senha/", AlterarSenhaView.as_view(), name="alterar-senha"),

    #rotas avaliacoes
    path("publicacoes/<int:publicacao_id>/avaliacoes/", AvaliacoesDaPublicacaoView.as_view(), name="avaliacoes-list"),
    path("publicacoes/<int:publicacao_id>/avaliacoes/criar/", AvaliacaoCreateView.as_view(), name="avaliacao-create"),
    path("avaliacoes/<int:pk>/editar/", AvaliacaoUpdateView.as_view(), name="avaliacao-update"),
    path("avaliacoes/<int:pk>/deletar/", AvaliacaoDeleteView.as_view(), name="avaliacao-delete"),

    #rotas autenticação
    path("signin/", Signin.as_view()),
    path("signup/", Signup.as_view()),

]
