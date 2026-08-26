from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        cpf_d = request.POST.get('cpf')
        senha_d = request.POST.get('password')
        
        if cpf_d:
            cpf_l = cpf_d.replace('.', '').replace('-', '')
        else:
            cpf_l = ''

        usuario = authenticate(request, username=cpf_l, password=senha_d)

        if usuario is not None:
            login(request, usuario)
            return redirect('dashboard') 
        else:
            messages.error(request, 'CPF ou senha inválidos. Tente novamente.')

    return render(request, 'login.html')