from django.contrib import admin

from . models import Aluno, Turma, Responsavel, Avaliacao

admin.site.register(Aluno);
admin.site.register(Turma);
admin.site.register(Responsavel);
admin.site.register(Avaliacao);