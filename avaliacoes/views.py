from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from .models import Responsavel, Aluno, Avaliacao, Turma, Professor
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
#import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils import timezone

# PDF generation (optional dependency)
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False
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
            messages.error(request, 'Usuário ou senha inválidos')
            return render(request, 'index.html')
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
                avaliacao.atualizado_por = request.user
                avaliacao.save()
            else:  # Criar novo
                # Obter o professor do usuário logado
                try:
                    professor = Professor.objects.get(user=request.user)
                except Professor.DoesNotExist:
                    professor = None
                
                Avaliacao.objects.create(
                    turma_id=request.POST.get('turma'),
                    aluno_id=request.POST.get('aluno'),
                    nota_conhecimento=request.POST.get('nota_conhecimento'),
                    nota_habilidade=request.POST.get('nota_habilidade'),
                    nota_engajamento=request.POST.get('nota_engajamento'),
                    nota_competencia=request.POST.get('nota_competencia'),
                    comentario=request.POST.get('comentario'),
                    professor=professor,
                    criado_por=request.user,
                    atualizado_por=request.user
                )

    lista_turmas = Turma.objects.all()
    lista_alunos = Aluno.objects.select_related('turma').all()
    lista_avaliacoes = Avaliacao.objects.select_related('aluno', 'turma', 'professor', 'professor__user', 'criado_por', 'atualizado_por').all()

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
                professor = Professor.objects.get(id=professor_id)
                usuario = professor.user
                professor.delete()
                usuario.delete()
            except:
                messages.info(request, 'Não é possível excluir o professor selecionado')
        # Criar ou atualizar professor
        else:
            professor_id = request.POST.get('professor_id')
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            materia = request.POST.get('materia')
            
            if professor_id:  # Atualizar
                professor = Professor.objects.get(id=professor_id)
                professor.user.first_name = nome.split()[0] if nome else ''
                professor.user.last_name = ' '.join(nome.split()[1:]) if len(nome.split()) > 1 else ''
                professor.user.email = email
                if senha:
                    professor.user.set_password(senha)
                professor.user.is_staff = True
                professor.user.is_active = True
                professor.user.save()
                professor.materia = materia
                professor.save()
            else:  # Criar novo
                # Criar usuário
                username = email.split('@')[0]
                usuario = User.objects.create_user(
                    username=username,
                    email=email,
                    password=senha,
                    first_name=nome.split()[0] if nome else '',
                    last_name=' '.join(nome.split()[1:]) if len(nome.split()) > 1 else '',
                    is_staff=True,
                    is_active=True
                )
                # Criar professor vinculado ao usuário
                Professor.objects.create(
                    user=usuario,
                    materia=materia
                )

    lista_professores = Professor.objects.select_related('user').all()
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
        lista_alunos = Aluno.objects.select_related('turma').all()
        lista_avaliacoes = Avaliacao.objects.all()  # lista inicial (todas)
        return render(request,'relatorios.html',{'lista_turmas':lista_turmas,'lista_alunos':lista_alunos,'lista_avaliacoes':lista_avaliacoes})
    #else:
    #    return render(request,'logoff.html')


def relatorios_data(request):
    """Retorna JSON com avaliações para turma+aluno (GET params)"""
    turma_id = request.GET.get('turma')
    aluno_id = request.GET.get('aluno')
    qs = Avaliacao.objects.all()
    if turma_id:
        qs = qs.filter(turma_id=turma_id)
    if aluno_id:
        qs = qs.filter(aluno_id=aluno_id)

    data = []
    for a in qs.select_related('professor','professor__user','criado_por','atualizado_por'):
        data.append({
            'id': a.id,
            'turma': a.turma.nome,
            'aluno': a.aluno.nome,
            'professor': a.professor.user.get_full_name() if a.professor else None,
            'materia': a.professor.materia if a.professor else None,
            'nota_conhecimento': a.nota_conhecimento,
            'nota_habilidade': a.nota_habilidade,
            'nota_engajamento': a.nota_engajamento,
            'nota_competencia': a.nota_competencia,
            'comentario': a.comentario,
            'data_criacao': a.data_criacao.isoformat() if a.data_criacao else None,
            'data_atualizacao': a.data_atualizacao.isoformat() if a.data_atualizacao else None,
            'criado_por': a.criado_por.get_full_name() if a.criado_por else None,
            'atualizado_por': a.atualizado_por.get_full_name() if a.atualizado_por else None,
        })

    return JsonResponse({'avaliacoes': data})


def relatorios_pdf(request):
    """Gera um PDF com as avaliações filtradas por turma e aluno (GET)."""
    if not REPORTLAB_AVAILABLE:
        return HttpResponse('Dependência reportlab não instalada', status=500)

    turma_id = request.GET.get('turma')
    aluno_id = request.GET.get('aluno')
    qs = Avaliacao.objects.all().select_related('turma','aluno','professor','professor__user','criado_por','atualizado_por')
    if turma_id:
        qs = qs.filter(turma_id=turma_id)
    if aluno_id:
        qs = qs.filter(aluno_id=aluno_id)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 2*cm

    title = 'Relatório de Avaliações'
    p.setFont('Helvetica-Bold', 14)
    p.drawString(2*cm, y, title)
    y -= 1*cm

    p.setFont('Helvetica', 10)
    for a in qs:
        lines = []
        lines.append(f'Aluno: {a.aluno.nome}  |  Turma: {a.turma.nome}')
        if a.professor:
            lines.append(f'Professor: {a.professor.user.get_full_name()}  |  Matéria: {a.professor.materia}')
        lines.append(f'Notas - Conhecimento: {a.nota_conhecimento}  Habilidade: {a.nota_habilidade}  Engajamento: {a.nota_engajamento}  Competência: {a.nota_competencia}')
        if a.comentario:
            lines.append(f'Comentário: {a.comentario}')
        lines.append(f'Criado: {a.data_criacao.strftime("%d/%m/%Y %H:%M")} por {a.criado_por.get_full_name() if a.criado_por else "-"}')
        lines.append(f'Atualizado: {a.data_atualizacao.strftime("%d/%m/%Y %H:%M")} por {a.atualizado_por.get_full_name() if a.atualizado_por else "-"}')

        for line in lines:
            p.drawString(2*cm, y, line)
            y -= 0.6*cm
            if y < 2*cm:
                p.showPage()
                y = height - 2*cm
                p.setFont('Helvetica', 10)

        # separator
        p.line(2*cm, y, width-2*cm, y)
        y -= 0.6*cm

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_avaliacoes.pdf"'
    response.write(pdf)
    return response