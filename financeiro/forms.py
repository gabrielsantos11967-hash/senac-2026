from django import forms
from django.core.exceptions import ValidationError

from financeiro.models import Funcionario, Lancamento


class FuncionarioAdminForm(forms.ModelForm):
    setor_nome = forms.CharField(max_length=100, label='Nome do setor')
    setor_descricao = forms.CharField(
        max_length=255,
        label='Descrição do setor',
        required=False,
    )
    lancamento_descricao = forms.CharField(
        max_length=255,
        label='Descrição do lançamento',
    )
    lancamento_valor = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Valor do lançamento',
    )
    lancamento_tipo = forms.ChoiceField(
        choices=(('Despesa', 'Despesa'), ('Receita', 'Receita')),
        label='Tipo do lançamento',
    )
    lancamento_data = forms.DateField(
        label='Data do lançamento',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    lancamento_conciliado = forms.BooleanField(
        label='Lançamento conciliado',
        required=False,
    )

    class Meta:
        model = Funcionario
        fields = ('nome', 'cargo', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['setor'].required = True

    def clean_lancamento_descricao(self):
        descricao = self.cleaned_data['lancamento_descricao']
        if Lancamento.objects.filter(descricao=descricao).exists():
            raise ValidationError('Já existe um lançamento com essa descrição.')
        return descricao
