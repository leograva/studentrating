from django.contrib import admin
from django.contrib.auth.models import User
from . models import Aluno, Turma, Responsavel, Avaliacao, Professor

admin.site.register(Aluno)
admin.site.register(Turma)
admin.site.register(Responsavel)
admin.site.register(Avaliacao)

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'materia', 'get_is_active')
    list_filter = ('materia', 'user__is_active')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'materia')
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Nome Completo'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'E-mail'
    
    def get_is_active(self, obj):
        return obj.user.is_active
    get_is_active.short_description = 'Ativo'
    get_is_active.boolean = True

admin.site.register(Professor, ProfessorAdmin)