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

    nome = models.CharField(max_length=100)
    materia = models.CharField(max_length=50, choices=MATERIAS_CHOICES)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    ativo = models.BooleanField(default=True) 

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores" # Define o nome plural personalizado

    def __str__(self):
        return self.nome

class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    nota_conhecimento = models.DecimalField(max_digits=1, decimal_places=0)
    nota_habilidades = models.DecimalField(max_digits=1, decimal_places=0)
    nota_engajamento = models.DecimalField(max_digits=1, decimal_places=0)
    nota_competencias = models.DecimalField(max_digits=1, decimal_places=0)
    comentario = models.TextField(blank=True, null=True)
    data = models.DateField()

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações" # Define o nome plural personalizado

    def __str__(self):
        return f'{self.aluno.nome} - {self.aluno.turma} - {self.data}'