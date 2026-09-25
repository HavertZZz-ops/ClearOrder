from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Estudante, Monitor, Tarefa, Quarto, Vistoria

def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'estudante'):
            return redirect('painel_estudante')
        elif hasattr(request.user, 'monitor'):
            return redirect('painel_monitor')
        else:
            return redirect('/admin/')

    if request.method == 'POST':
        cpf_digitado = request.POST.get('cpf')
        senha_digitada = request.POST.get('password')
        username_para_login = cpf_digitado

        try:
            estudante_encontrado = Estudante.objects.get(cpf=cpf_digitado)
            username_para_login = estudante_encontrado.user.username
        except Estudante.DoesNotExist:
            try:
                monitor_encontrado = Monitor.objects.get(cpf=cpf_digitado)
                username_para_login = monitor_encontrado.user.username
            except Monitor.DoesNotExist:
                pass

        usuario = authenticate(request, username=username_para_login, password=senha_digitada)

        if usuario is not None:
            login(request, usuario)
            if hasattr(usuario, 'estudante'):
                return redirect('painel_estudante')
            elif hasattr(usuario, 'monitor'):
                return redirect('painel_monitor')
            else:
                return redirect('/admin/')
        else:
            messages.error(request, 'CPF ou senha inválidos. Tente novamente.')

    return render(request, 'login.html')

def fazer_logout(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('login')

@login_required
def painel_estudante(request):
    if hasattr(request.user, 'estudante'):
        estudante = request.user.estudante
        tarefas = Tarefa.objects.filter(estudante_responsavel=estudante)
        contexto = {
            'estudante': estudante,
            'tarefas': tarefas
        }
        return render(request, 'painel_estudante.html', contexto)
    elif hasattr(request.user, 'monitor'):
        return redirect('painel_monitor')
    else:
        logout(request)
        messages.error(request, 'Acesso negado: Sua conta não possui um perfil válido. Procure a administração.')
        return redirect('login')
@login_required
def concluir_tarefa(request, tarefa_id):
    if not hasattr(request.user, 'estudante'):
        messages.error(request, 'Apenas estudantes podem concluir tarefas.')
        return redirect('login')

   
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, estudante_responsavel=request.user.estudante)

   
    if tarefa.status == 'Concluída':
        tarefa.status = 'Pendente'
    else:
        tarefa.status = 'Concluída'
    
    tarefa.save()

    messages.success(request, 'Status da tarefa atualizado com sucesso!')
    return redirect('painel_estudante')
@login_required
def painel_monitor(request):
    if hasattr(request.user, 'monitor'):
        
        estudantes = Estudante.objects.all()
        
    
        total_pendentes = Tarefa.objects.filter(status='Pendente').count()

        contexto = {
            'estudantes': estudantes,
            'total_pendentes': total_pendentes,
            'total_quartos': estudantes.count(),
          
        }
        return render(request, 'painel_monitor.html', contexto)
        
    elif hasattr(request.user, 'estudante'):
        return redirect('painel_estudante')
    else:
        logout(request)
        messages.error(request, 'Acesso negado.')
        return redirect('login')
@login_required
def detalhes_quarto(request, quarto_id):
    if hasattr(request.user, 'monitor'):
        quarto_selecionado = get_object_or_404(Quarto, id=quarto_id)

        if request.method == 'POST':
            nota = request.POST.get('nota')
            observacoes = request.POST.get('observacoes')
            aprovado = request.POST.get('aprovado') == 'True'

            Vistoria.objects.create(
                monitor=request.user.monitor,
                quarto=quarto_selecionado,
                nota=nota,
                observacoes=observacoes,
                aprovado=aprovado
            )

          
            if aprovado:
                quarto_selecionado.streak += 1
            else:
                quarto_selecionado.streak = 0
            quarto_selecionado.save()

            messages.success(request, 'Vistoria guardada com sucesso!')
            return redirect('painel_monitor')

        estudantes = Estudante.objects.all()
        total_pendentes = Tarefa.objects.filter(status='Pendente').count()

        contexto = {
            'estudantes': estudantes,
            'total_pendentes': total_pendentes,
            'total_quartos': estudantes.count(),
            'quarto_selecionado': quarto_selecionado 
        }

      
        return render(request, 'painel_monitor.html', contexto)

    elif hasattr(request.user, 'estudante'):
        return redirect('painel_estudante')
    else:
        logout(request)
        return redirect('login')
@login_required
def reportar_problema(request):
    # Trava de segurança: apenas estudantes acessam essa tela
    if hasattr(request.user, 'estudante'):
        
        # Quando o aluno preencher o formulário e clicar em "Enviar Relatório"
        if request.method == 'POST':
            titulo = request.POST.get('titulo')
            categoria = request.POST.get('categoria')
            descricao = request.POST.get('descricao')
            
            # Aqui você salvará no banco de dados. 
            # Exemplo (remova os comentários quando criar a tabela no models.py):
            # Problema.objects.create(
            #     estudante_responsavel=request.user.estudante,
            #     titulo=titulo,
            #     categoria=categoria,
            #     descricao=descricao,
            #     status='Aberto'
            # )
            
            messages.success(request, 'Problema reportado com sucesso! A manutenção foi notificada.')
            return redirect('painel_estudante')
            
        # Se for apenas um clique no menu (GET), carrega a tela do Vitor vazia
        return render(request, 'reportar_problema.html')
        
    elif hasattr(request.user, 'monitor'):
        messages.warning(request, 'Monitores não podem reportar problemas por esta tela.')
        return redirect('painel_monitor')
    
    else:
        return redirect('login')
    