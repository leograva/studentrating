from django.db import models

# Create your models here.

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas" # Define o nome plural personalizado

    def __str__(self):
        return self.nome
    
class Responsavel(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis" # Define o nome plural personalizado

    def __str__(self):
        return self.nome + ' - ' + self.email

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos" # Define o nome plural personalizado

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(getattr(self, field.name, ' ')))
        return ' - '.join(field_values)

class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=1, decimal_places=0)
    comentario = models.TextField(blank=True, null=True)
    data = models.DateField()

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações" # Define o nome plural personalizado

    def __str__(self):
        return f'{self.aluno.nome} - {self.aluno.turma} - {self.nota} - {self.data}'