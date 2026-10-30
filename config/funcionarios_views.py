from django.db import connection
from django.shortcuts import render


def get_funcionarios():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, nome, cargo, email
            FROM funcionarios
            ORDER BY nome, id
            """
        )
        columns = [column[0] for column in cursor.description]
        funcionarios = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return funcionarios


def funcionarios_list(request):
    return render(
        request,
        'financeiro/funcionarios.html',
        {'funcionarios': get_funcionarios()},
    )
