from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from .models import Responsavel, Aluno, Avaliacao, Turma, Professor
from django.contrib.auth import get_user_model
#import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def logoff(request):
    return HttpResponseRedirect('login')

def sair(request):
    logout(request)
    return HttpResponseRedirect('login')

def cadastrar_usuario(request):  
    if request.user.is_authenticated:
        if request.method == "POST":
            form_usuario = UserCreationForm(request.POST)
            if form_usuario.is_valid():
                form_usuario.save()
                return HttpResponseRedirect('login')
        else:
            form_usuario = UserCreationForm()
        return render(request, 'cadastro.html', {'form_usuario': form_usuario})
    else:
        return HttpResponseRedirect('login')

def index(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('menu')
        else:
            return HttpResponseRedirect('login')
    else:
        return render(request, 'index.html')
    
# Menu
def menu(request):
    if request.user.is_authenticated:
        return render(request,'menu.html')
    else:
        return render(request,'logoff.html')

def responsaveis(request):
    #if request.user.is_authenticated:
    if request.method == 'POST':
        # Excluir responsável
        if 'excluir_responsavel' in request.POST:
            responsavel_id = request.POST.get('responsavel_id')
            try:
                Responsavel.objects.get(id=responsavel_id).delete()
            except:
                messages.info(request, 'Não é possível excluir o responsável selecionado pois ele está sendo utilizado em algum aluno cadastrado')
        # Criar ou atualizar responsável
        else:
            responsavel_id = request.POST.get('responsavel_id')
            if responsavel_id:  # Atualizar
                responsavel = Responsavel.objects.get(id=responsavel_id)
                responsavel.nome = request.POST.get('nome')
                responsavel.email = request.POST.get('email')
                responsavel.save()
            else:  # Criar novo
                responsavel = Responsavel()
                responsavel.nome = request.POST.get('nome')
                responsavel.email = request.POST.get('email')
                responsavel.save()
    
    lista_responsaveis = Responsavel.objects.all()
    return render(request,'responsaveis.html',{'lista_responsaveis':lista_responsaveis})
    #else:
    #    return render(request,'logoff.html')

def turmas(request):
    if request.method == 'POST':
        # Excluir turma
        if 'excluir_turma' in request.POST:
            turma_id = request.POST.get('turma_id')
            try:
                Turma.objects.get(id=turma_id).delete()
            except:
                messages.info(request, 'Não é possível excluir a turma selecionada pois ela está sendo utilizada')
        # Criar ou atualizar turma
        else:
            turma_id = request.POST.get('turma_id')
            if turma_id:  # Atualizar
                turma = Turma.objects.get(id=turma_id)
                turma.nome = request.POST.get('nome')
                turma.save()
            else:  # Criar novo
                turma = Turma()
                turma.nome = request.POST.get('nome')
                turma.save()

    lista_turmas = Turma.objects.all()
    return render(request, 'turmas.html', {'lista_turmas': lista_turmas})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Avaliacao, Turma, Aluno


def avaliacoes(request):
    if request.method == 'POST':
        # Excluir avaliação
        if 'excluir_avaliacao' in request.POST:
            avaliacao_id = request.POST.get('avaliacao_id')
            Avaliacao.objects.filter(id=avaliacao_id).delete()
        
        # Criar ou atualizar avaliação
        else:
            avaliacao_id = request.POST.get('avaliacao_id')
            if avaliacao_id:  # Atualizar
                avaliacao = Avaliacao.objects.get(id=avaliacao_id)
                avaliacao.turma_id = request.POST.get('turma')
                avaliacao.aluno_id = request.POST.get('aluno')
                avaliacao.nota_conhecimento = request.POST.get('nota_conhecimento')
                avaliacao.nota_habilidade = request.POST.get('nota_habilidade')
                avaliacao.nota_engajamento = request.POST.get('nota_engajamento')
                avaliacao.nota_competencia = request.POST.get('nota_competencia')
                avaliacao.comentario = request.POST.get('comentario')
                avaliacao.save()
            else:  # Criar novo
                Avaliacao.objects.create(
                    turma_id=request.POST.get('turma'),
                    aluno_id=request.POST.get('aluno'),
                    nota_conhecimento=request.POST.get('nota_conhecimento'),
                    nota_habilidade=request.POST.get('nota_habilidade'),
                    nota_engajamento=request.POST.get('nota_engajamento'),
                    nota_competencia=request.POST.get('nota_competencia'),
                    comentario=request.POST.get('comentario')
                )

    lista_turmas = Turma.objects.all()
    lista_alunos = Aluno.objects.select_related('turma').all()
    lista_avaliacoes = Avaliacao.objects.select_related('aluno', 'turma').all()

    return render(request, 'avaliacoes.html', {
        'lista_turmas': lista_turmas,
        'lista_alunos': lista_alunos,
        'lista_avaliacoes': lista_avaliacoes
    })


def professores(request):
    if request.method == 'POST':
        # Excluir professor
        if 'excluir_professor' in request.POST:
            professor_id = request.POST.get('professor_id')
            try:
                Professor.objects.get(id=professor_id).delete()
            except:
                messages.info(request, 'Não é possível excluir o professor selecionado')
        # Criar ou atualizar professor
        else:
            professor_id = request.POST.get('professor_id')
            if professor_id:  # Atualizar
                professor = Professor.objects.get(id=professor_id)
                professor.nome = request.POST.get('nome')
                professor.email = request.POST.get('email')
                professor.senha = request.POST.get('senha')
                professor.materia = request.POST.get('materia')
                professor.ativo = True if request.POST.get('ativo') == 'on' else False
                professor.save()
            else:  # Criar novo
                professor = Professor()
                professor.nome = request.POST.get('nome')
                professor.email = request.POST.get('email')
                professor.senha = request.POST.get('senha')
                professor.materia = request.POST.get('materia')
                professor.ativo = True if request.POST.get('ativo') == 'on' else False
                professor.save()

    lista_professores = Professor.objects.all()
    return render(request, 'professores.html', {'lista_professores': lista_professores})

def alunos(request):
    if request.method == 'POST':
        # Excluir aluno
        if 'excluir_aluno' in request.POST:
            aluno_id = request.POST.get('aluno_id')
            try:
                Aluno.objects.get(id=aluno_id).delete()
            except:
                messages.info(request, 'Não é possível excluir o aluno selecionado')
        # Criar ou atualizar aluno
        else:
            aluno_id = request.POST.get('aluno_id')
            if aluno_id:  # Atualizar
                aluno = Aluno.objects.get(id=aluno_id)
                aluno.nome = request.POST.get('nome')
                aluno.turma_id = request.POST.get('turma')
                aluno.responsavel_id = request.POST.get('responsavel')
                aluno.save()
            else:  # Criar novo
                Aluno.objects.create(
                    nome=request.POST.get('nome'),
                    turma_id=request.POST.get('turma'),
                    responsavel_id=request.POST.get('responsavel')
                )

    lista_alunos = Aluno.objects.select_related('turma', 'responsavel').all()
    lista_turmas = Turma.objects.all()
    lista_responsaveis = Responsavel.objects.all()

    return render(
        request,
        'alunos.html',
        {
            'lista_alunos': lista_alunos,
            'lista_turmas': lista_turmas,
            'lista_responsaveis': lista_responsaveis
        }
    )

def relatorios(request):
    #if request.user.is_authenticated:
        lista_turmas = Turma.objects.all()
        return render(request,'relatorios.html',{'lista_turmas':lista_turmas})
    #else:
    #    return render(request,'logoff.html')