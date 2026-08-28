@echo off
title Iniciar Projeto ClearOrder
echo =========================================
echo   Preparando o ambiente Django...
echo =========================================

:: 1. Verifica e ativa o ambiente virtual na raiz (.venv)
if exist ".venv\Scripts\activate" (
    echo [*] Ativando o ambiente virtual...
    call .venv\Scripts\activate
) else (
    echo [!] Ambiente virtual ".venv" nao encontrado na raiz!
    pause
    exit
)

:: 2. Instala dependencias se houver requirements.txt na raiz
if exist "requirements.txt" (
    echo [*] Verificando e instalando dependencias...
    pip install -r requirements.txt
)

:: 3. Acessa a pasta config e inicia o servidor
if exist "config\manage.py" (
    echo [*] Acessando a pasta config...
    cd config
    echo [*] Iniciando o servidor Django...
    python manage.py runserver
) else (
    echo [!] "manage.py" nao encontrado dentro da pasta "config".
)

pause
