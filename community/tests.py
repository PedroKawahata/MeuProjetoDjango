from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Answer, Post


class CommunityTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(username="autor")
        self.student = user_model.objects.create_user(username="colega")
        self.post = Post.objects.create(
            title="Como estudar lógica?",
            content="Preciso de ajuda com condicionais.",
            category="duvida",
            author=self.owner,
        )

    def test_visitante_vai_para_o_login(self):
        url = reverse("community:feed")
        login_url = reverse("accounts:login")

        response = self.client.get(url)

        self.assertRedirects(response, f"{login_url}?next={url}")

    def test_colega_nao_pode_editar_post(self):
        self.client.force_login(self.student)
        url = reverse("community:edit", args=[self.post.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_resposta_e_salva_com_autor_logado(self):
        self.client.force_login(self.student)
        url = reverse("community:detail", args=[self.post.pk])

        response = self.client.post(url, {"content": "Tente começar com if e else."})

        self.assertRedirects(response, url)
        answer = Answer.objects.get(post=self.post)
        self.assertEqual(answer.author, self.student)

    def test_autor_pode_trocar_solucao(self):
        previous = Answer.objects.create(
            post=self.post, author=self.student, content="Primeira opção", is_solution=True
        )
        selected = Answer.objects.create(
            post=self.post, author=self.student, content="Segunda opção"
        )
        self.client.force_login(self.owner)
        url = reverse("community:mark_solution", args=[selected.pk])

        response = self.client.post(url)

        self.assertRedirects(response, reverse("community:detail", args=[self.post.pk]))
        previous.refresh_from_db()
        selected.refresh_from_db()
        self.post.refresh_from_db()
        self.assertFalse(previous.is_solution)
        self.assertTrue(selected.is_solution)
        self.assertTrue(self.post.is_resolved)