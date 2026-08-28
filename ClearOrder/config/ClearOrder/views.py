from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'estudante'):
            return redirect('painel_estudante')
        elif hasattr(request.user, 'monitor'):
            return redirect('painel_monitor')
        else:
            return redirect('/admin/')

    if request.method == 'POST':
        cpf_d = request.POST.get('cpf')
        senha_d = request.POST.get('password')
        
        usuario = authenticate(request, username=cpf_d, password=senha_d)

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



@login_required
def painel_estudante(request):
    if hasattr(request.user, 'estudante'):
        return render(request, 'painel_estudante.html')
    elif hasattr(request.user, 'monitor'):
        return redirect('painel_monitor')
    else:
        logout(request) 
        messages.error(request, 'Acesso negado: Sua conta não possui um perfil válido. Procure a administração.')
        return redirect('login') 



@login_required
def painel_monitor(request):
    if hasattr(request.user, 'monitor'):
        return render(request, 'painel_monitor.html')
    elif hasattr(request.user, 'estudante'):
        return redirect('painel_estudante')
    else:
        logout(request)
        messages.error(request, 'Acesso negado: Sua conta não possui um perfil válido. Procure a administração.')
        return redirect('login')