from django.urls import path # <- Importa a função que associa Textos (urls) a funções python 
from django.contrib.auth import views as auth_views # <- Importa o pacote oficial de segurança do Django, traz prontas as visões de login e etc
from .views import SignUpView # <- Importa a classe de views

app_name = 'accounts' # <- Cria uma "Etiqueta" para não causar conflitos de rota no app

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'), # <= Aponta para o login padrão do Django, onde está o template visual e o login.html


    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # <= Mapeia o endereço /accounts/logout para destruir a sessão ativa do usuário com segurança


    path('signup/', SignUpView.as_view(), name='signup'), # <=  mapeia o endereço /accounts/signup para classe de cadastro
]