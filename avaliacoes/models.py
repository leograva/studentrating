from django.db import models
from django.contrib.auth.models import User

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
        verbose_name_plural = "Alunos"

    def __str__(self):
        return f'{self.nome} - {self.turma}'
    
class Professor(models.Model):

    MATERIAS_CHOICES = [
        ('Matemática', 'Matemática'),
        ('Português', 'Português'),
        ('História', 'História'),
        ('Geografia', 'Geografia'),
        ('Física', 'Física'),
        ('Química', 'Química'),
        ('Biologia', 'Biologia'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    materia = models.CharField(max_length=50, choices=MATERIAS_CHOICES)

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores" # Define o nome plural personalizado

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Avaliacao(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)

    nota_conhecimento = models.IntegerField()
    nota_habilidade = models.IntegerField()
    nota_engajamento = models.IntegerField()
    nota_competencia = models.IntegerField()

    comentario = models.TextField(blank=True, null=True)
    
    # Campos de auditoria
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='avaliacoes_criadas')
    atualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='avaliacoes_atualizadas')