from django.contrib.auth.forms import UserCreationForm # <- Importa o formulário de criação de usuário do Django    
from django.urls import reverse_lazy # <-Importa a função que calcula pra qual endereço o usuário sera redirecionado após o cadastro 
from django.views.generic import CreateView # <- Importa a classe genérica para salvar e criar registros no banco de dados sem precisar escrever SQL

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'