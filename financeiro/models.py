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


class Lancamento(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255, unique=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50)
    data = models.DateField()
    conciliado = models.BooleanField(default=False)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'financeiro'
        verbose_name = 'lançamento'
        verbose_name_plural = 'lançamentos'
        ordering = ('data', 'id')

    def __str__(self):
        return self.descricao
