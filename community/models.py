from django.conf import settings
from django.db import models


class Post(models.Model):
    CATEGORY_CHOICES = [
        ("duvida", "Dúvida"),
        ("atividade", "Atividade"),
        ("conteudo", "Conteúdo"),
        ("material", "Material de estudo"),
    ]

    title = models.CharField("Título", max_length=150)
    content = models.TextField("Descrição")
    category = models.CharField("Categoria", max_length=20, choices=CATEGORY_CHOICES)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="taregran_posts",
        verbose_name="Autor",
    )

    is_resolved = models.BooleanField("Resolvida", default=False)
    created_at = models.DateTimeField("Criada em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizada em", auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title