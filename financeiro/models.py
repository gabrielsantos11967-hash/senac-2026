from django.db import models


class Setor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'setor'
        verbose_name = 'setor'
        verbose_name_plural = 'setores'
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    cargo = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        db_column='setor_id',
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = 'funcionarios'
        verbose_name = 'funcionário'
        verbose_name_plural = 'funcionários'
        ordering = ('nome', 'id')

    def __str__(self):
        return self.nome


class Lancamento(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255, unique=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50)
    data = models.DateField()
    conciliado = models.BooleanField(default=False)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = 'financeiro'
        verbose_name = 'lançamento'
        verbose_name_plural = 'lançamentos'
        ordering = ('data', 'id')

    def __str__(self):
        return self.descricao
