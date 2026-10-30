from django.contrib import admin
from django.db import transaction

from financeiro.forms import FuncionarioAdminForm
from financeiro.models import Funcionario, Lancamento, Setor


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    list_display = (
        'descricao',
        'valor',
        'tipo',
        'data',
        'conciliado',
        'setor',
        'funcionario',
    )
    list_filter = ('tipo', 'conciliado', 'setor')
    search_fields = ('descricao', 'funcionario__nome')
    date_hierarchy = 'data'
    autocomplete_fields = ('setor', 'funcionario')


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    form = FuncionarioAdminForm
    list_display = ('nome', 'cargo', 'email', 'setor')
    list_filter = ('setor',)
    search_fields = ('nome', 'cargo', 'email', 'setor__nome')

    def get_fields(self, request, obj=None):
        if obj is not None:
            return ('nome', 'cargo', 'email', 'setor')
        return (
            'nome',
            'cargo',
            'email',
            'setor_nome',
            'setor_descricao',
            'lancamento_descricao',
            'lancamento_valor',
            'lancamento_tipo',
            'lancamento_data',
            'lancamento_conciliado',
        )

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            if change:
                super().save_model(request, obj, form, change)
                Lancamento.objects.filter(funcionario=obj).update(setor=obj.setor)
                return

            setor, _ = Setor.objects.get_or_create(
                nome=form.cleaned_data['setor_nome'],
                defaults={
                    'descricao': form.cleaned_data['setor_descricao'] or None,
                },
            )
            obj.setor = setor
            super().save_model(request, obj, form, change)
            Lancamento.objects.create(
                descricao=form.cleaned_data['lancamento_descricao'],
                valor=form.cleaned_data['lancamento_valor'],
                tipo=form.cleaned_data['lancamento_tipo'],
                data=form.cleaned_data['lancamento_data'],
                conciliado=form.cleaned_data['lancamento_conciliado'],
                setor=setor,
                funcionario=obj,
            )
