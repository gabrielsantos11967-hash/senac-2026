from django.db import connection
from django.shortcuts import render


def financeiro_list(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                financeiro.id,
                financeiro.descricao,
                financeiro.valor,
                financeiro.tipo,
                financeiro.data,
                financeiro.conciliado,
                setor.nome AS setor
            FROM financeiro
            INNER JOIN setor ON setor.id = financeiro.setor_id
            ORDER BY financeiro.data, financeiro.id
            """
        )
        columns = [column[0] for column in cursor.description]
        lancamentos = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return render(request, 'financeiro/lista.html', {'lancamentos': lancamentos})
