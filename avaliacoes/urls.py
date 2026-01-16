from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('login',views.index, name='index'),

    path('menu',views.menu, name='menu'),

    #logoff
    path('sair',views.sair,name='sair'),
    
    #logout
    path('logoff',views.logoff,name='logoff'),

    path('responsaveis',views.responsaveis,name='responsaveis'),
    path('turmas',views.turmas,name='turmas'),
    path('avaliacoes',views.avaliacoes,name='avaliacoes'),
    path('professores',views.professores,name='professores'),
    path('alunos',views.alunos,name='alunos'),
    path('relatorios',views.relatorios,name='relatorios')
    ]