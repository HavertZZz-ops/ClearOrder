from django.contrib import admin
from .models import Quarto, Estudante, Monitor, Cronograma, TarefaLimpeza, Vistoria, Notificacao, SolicitacaoReparo


admin.site.register(Quarto)
admin.site.register(Estudante)
admin.site.register(Monitor)
admin.site.register(Cronograma)
admin.site.register(TarefaLimpeza)
admin.site.register(Vistoria)
admin.site.register(Notificacao)
admin.site.register(SolicitacaoReparo)
# Register your models here.
