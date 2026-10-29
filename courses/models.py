from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(verbose_name="Nome", max_length=30)
    last_name = models.CharField(verbose_name="Sobrenome", max_length=30)

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ["first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    PERIOD_CHOICES = [
        ("M", "Matutino"),
        ("V", "Vespertino"),
        ("N", "Noturno"),
    ]

    name = models.CharField(verbose_name="Nome do curso", max_length=100)
    description = models.TextField(verbose_name="Descrição", blank=True)
    workload = models.PositiveIntegerField(verbose_name="Carga horária (h)", default=0)
    period = models.CharField(
        verbose_name="Período",
        max_length=1,
        choices=PERIOD_CHOICES,
        default="M",
    )
    teacher = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name="Professor",
    )

    capa = models.ImageField(upload_to='capas/', null=True, blank=True) # 👈 upload_to define a subpasta dentro de media/

    material = models.FileField(upload_to='materials/', null=True, blank=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["name"]

    def __str__(self):
        return self.name

material = models.FileField(
    upload_to="courses/materials/",
)

image = models.ImageField(
    upload_to="courses/images/",
)