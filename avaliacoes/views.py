from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from huggingface_hub import User
from .models import Responsavel, Aluno, Avaliacao, Turma
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

## Responsável    
def responsaveis(request):
    #if request.user.is_authenticated:
    if request.method == 'POST':
            if request.POST.get('nome'):
                responsavel = Responsavel()
                responsavel.nome = request.POST.get('nome')
                responsavel.email = request.POST.get('email')
                responsavel.save()
                lista_responsaveis = Responsavel.objects.all()
                return render(request,'responsaveis.html',{'lista_responsaveis':lista_responsaveis})
    else:
        lista_responsaveis = Responsavel.objects.all()
        return render(request,'responsaveis.html',{'lista_responsaveis':lista_responsaveis})
    #else:
    #    return render(request,'logoff.html')

def deletar_responsavel(request,id):
    #if request.user.is_authenticated:
        try:
            registro = Responsavel.objects.get(id =id)
            registro.delete()
            responsaveis = Responsavel.objects.all().order_by('nome')
            return redirect(request.META['HTTP_REFERER'])
        except:
            messages.info(request, 'Não é possível excluir o responsável selecionado pois ele está sendo utilizado em algum aluno cadastrado')
            #responsaveis = Responsavel.objects.all()
            return render(request,'responsaveis.html')#,{'responsaveis':responsaveis})
    #else:
    #    return render(request,'logoff.html')
    
## Turma  
def turmas(request):
    #if request.user.is_authenticated:
        lista_turmas = Turma.objects.all()
        return render(request,'turmas.html',{'lista_turmas':lista_turmas})
    #else:
    #    return render(request,'logoff.html')

## Avaliação  
def avaliacoes(request):
    #if request.user.is_authenticated:
        lista_avaliacoes = Avaliacao.objects.all()
        lista_alunos = Aluno.objects.all()
        lista_turmas = Turma.objects.all()
        return render(request,'avaliacoes.html',{'lista_avaliacoes':lista_avaliacoes, 'lista_alunos': lista_alunos, 'lista_turmas':lista_turmas})
    #else:
    #    return render(request,'logoff.html')

## Professor
def professores(request):
    #if request.user.is_authenticated: 
        
        User = get_user_model()
        lista_professores = User.objects.all()
        
        return render(request,'professores.html',{'lista_professores':lista_professores})
    #else:
    #    return render(request,'logoff.html')


## Aluno
def alunos(request):
    #if request.user.is_authenticated:
        lista_turmas = Turma.objects.all()
        lista_alunos = Aluno.objects.all()
        return render(request,'alunos.html',{'lista_alunos':lista_alunos,'lista_turmas':lista_turmas})
    #else:
    #    return render(request,'logoff.html')

def guia_avaliacao(request):
     return render(request,'guia_avaliacao.html')

def relatorios(request):
    #if request.user.is_authenticated:
        lista_turmas = Turma.objects.all()
        return render(request,'relatorios.html',{'lista_turmas':lista_turmas})
    #else:
    #    return render(request,'logoff.html')