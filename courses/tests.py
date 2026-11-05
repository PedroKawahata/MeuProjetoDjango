from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse


class CourseAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="aluno_teste",
            password="SenhaSomenteParaTeste123!",
        )

    def test_visitante_precisa_entrar(self):
        url = reverse("courses:course_list")

        response = self.client.get(url)

        login_url = reverse("accounts:login")
        self.assertRedirects(
            response,
            f"{login_url}?next={url}",
        )

    def test_aluno_sem_permissao_recebe_403(self):
        self.client.force_login(self.user)

        url = reverse("courses:course_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_aluno_com_permissao_pode_listar(self):
        permission = Permission.objects.get(
            content_type__app_label="courses",
            codename="view_course",
        )
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)

        url = reverse("courses:course_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "courses/course_list.html",
        )