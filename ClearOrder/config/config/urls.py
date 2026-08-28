from django.contrib import admin
from django.urls import path


from ClearOrder.views import login_view, painel_estudante, painel_monitor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('aluno/', painel_estudante, name='painel_estudante'),
    path('monitor/', painel_monitor, name='painel_monitor'),
]