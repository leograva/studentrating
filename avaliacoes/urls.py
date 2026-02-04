from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('responsaveis', views.responsaveis, name='responsaveis'),
    path('turmas', views.turmas, name='turmas'),
    path('avaliacoes', views.avaliacoes, name='avaliacoes'),
    path('professores', views.professores, name='professores'),
    path('alunos', views.alunos, name='alunos'),
    path('relatorios', views.relatorios, name='relatorios'),
    path('relatorios/data', views.relatorios_data, name='relatorios_data'),
    path('relatorios/pdf', views.relatorios_pdf, name='relatorios_pdf'),
]