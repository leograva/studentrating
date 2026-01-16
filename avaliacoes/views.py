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

        print(username,password)

        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            print("autenticou")
            return redirect('menu')
        else:
            print("nao autenticou")
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
        lista_responsaveis = Responsavel.objects.all()
        return render(request,'responsaveis.html',{'lista_responsaveis':lista_responsaveis})
    #else:
    #    return render(request,'logoff.html')

def turmas(request):
    #if request.user.is_authenticated:
        lista_turmas = Turma.objects.all()
        return render(request,'turmas.html',{'lista_turmas':lista_turmas})
    #else:
    #    return render(request,'logoff.html')

def avaliacoes(request):
    #if request.user.is_authenticated:
        lista_avaliacoes = Avaliacao.objects.all()
        lista_alunos = Aluno.objects.all()
        lista_turmas = Turma.objects.all()
        return render(request,'avaliacoes.html',{'lista_avaliacoes':lista_avaliacoes, 'lista_alunos': lista_alunos, 'lista_turmas':lista_turmas})
    #else:
    #    return render(request,'logoff.html')

def professores(request):
    #if request.user.is_authenticated:
        
        User = get_user_model()
        lista_professores = User.objects.all()
        
        print(lista_professores)
        return render(request,'professores.html',{'lista_professores':lista_professores})
    #else:
    #    return render(request,'logoff.html')

def alunos(request):
    #if request.user.is_authenticated:
        lista_turmas = Turma.objects.all()
        lista_alunos = Aluno.objects.all()
        return render(request,'alunos.html',{'lista_alunos':lista_alunos,'lista_turmas':lista_turmas})
    #else:
    #    return render(request,'logoff.html')

def relatorios(request):
    #if request.user.is_authenticated:
        lista_turmas = Turma.objects.all()
        return render(request,'relatorios.html',{'lista_turmas':lista_turmas})
    #else:
    #    return render(request,'logoff.html')