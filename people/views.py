from django.contrib.auth.mixins import LoginRequiredMixin # Importa a "Segurança de catraca" direto do Django para classes de visualização
from django.views.generic import ListView
from courses.models import Person

class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    template_name = "person/list_view.html"
    context_object_name = "people"
    paginate_by = 1