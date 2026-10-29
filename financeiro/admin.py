from django.contrib import admin

from financeiro.models import Lancamento, Setor


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'tipo', 'data', 'conciliado', 'setor')
    list_filter = ('tipo', 'conciliado', 'setor')
    search_fields = ('descricao',)
    date_hierarchy = 'data'
    autocomplete_fields = ('setor',)
