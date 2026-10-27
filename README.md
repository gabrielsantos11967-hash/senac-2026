# CRUD financeiro com Python e PostgreSQL

O projeto demonstra a conexao a um banco PostgreSQL e as operacoes CRUD em
lancamentos financeiros relacionados a setores. O script Python cria as tabelas,
insere dados de exemplo e exibe os resultados das consultas e alteracoes.
Os arquivos estao separados: o codigo Python fica em `python/` e os comandos
para conferencia no SQLTools ficam em `postgresql/`.

## Conexao

Foi usada a biblioteca **Psycopg 3** (`psycopg`), driver para PostgreSQL que
permite executar SQL parametrizado em Python. Os valores usados pelo SQLTools
estao em `.vscode/settings.json`; preencha as mesmas configuracoes no arquivo
local `.env`, sem colocar a senha neste README:

| Dado de conexao | Valor |
| --- | --- |
| SGBD/driver | PostgreSQL |
| Host | `172.16.80.50` |
| Porta | `5432` |
| Banco | `equipe02` |
| Usuario | `equipe02` |
| Senha | Variavel local `DB_PASSWORD` (nao compartilhar) |

O arquivo `.env` ja deve ficar na raiz do projeto e e ignorado pelo Git.
Use `.env.example` como modelo se precisar configurar outro computador:

```env
DB_HOST=172.16.80.50
DB_PORT=5432
DB_NAME=equipe02
DB_USER=equipe02
DB_PASSWORD=
```

Mantenha a senha apenas no `.env` local. Nao tire print desse arquivo nem
compartilhe seu conteudo. Instale as dependencias e execute o programa no
terminal integrado do VS Code:

```powershell
python -m pip install -r .\python\requirements.txt
python .\python\crud_financeiro.py
```

O script imprime host, porta, banco e usuario, mas nunca imprime a senha. Para
registrar a conexao, tire um print do SQLTools conectado e outro do terminal
mostrando a execucao bem-sucedida do script.

## Tabelas

O comando completo esta em
[`postgresql/02.session.sql`](./postgresql/02.session.sql), e a criacao tambem
e feita pelo script Python em [`python/crud_financeiro.py`](./python/crud_financeiro.py).
A tabela principal `financeiro` contem:

| Coluna | Tipo | Justificativa |
| --- | --- | --- |
| `id` | `INTEGER ... IDENTITY PRIMARY KEY` | Numero inteiro gerado pelo banco e usado como identificador unico. |
| `descricao` | `VARCHAR(255)` | Texto curto para identificar o lancamento. |
| `valor` | `NUMERIC(10, 2)` | Valor monetario com duas casas decimais. |
| `tipo` | `VARCHAR(50)` | Texto que classifica o lancamento como receita ou despesa. |
| `data` | `DATE` | Armazena a data sem horario. |
| `conciliado` | `BOOLEAN` | Representa uma informacao que so pode ser verdadeira ou falsa. |
| `setor_id` | `INTEGER` | Chave estrangeira que relaciona o lancamento ao setor responsavel. |

`setor` e a tabela relacionada. Seu `id` tambem e gerado pelo banco, e
`financeiro.setor_id` referencia `setor.id`. Para mostrar a estrutura, abra
`postgresql/02.session.sql` no SQLTools e execute os comandos de criacao; depois
consulte as tabelas em **Tables** e salve um print legivel das colunas e tipos.

## CRUD: trechos e conferencias

Os comandos abaixo correspondem ao script Python. Ele usa parametros (`%s`)
para enviar os valores ao banco separadamente do SQL.

### Create

`seed_data` insere tres setores e cinco lancamentos de exemplo, sem informar
os IDs. O banco gera as chaves primarias. Se o script for executado novamente,
os exemplos que ja existem nao sao duplicados.

```sql
INSERT INTO financeiro (descricao, valor, tipo, data, conciliado, setor_id)
SELECT %s, %s, %s, %s, %s, setor.id
FROM setor
WHERE setor.nome = %s
  AND NOT EXISTS (
      SELECT 1 FROM financeiro existente
      WHERE existente.descricao = %s
  );
```

No SQLTools, confira as linhas com `SELECT * FROM financeiro ORDER BY id;` e
tire um print depois de executar o script.

### Read

O programa mostra tres consultas: todos os registros, despesas filtradas com
`WHERE tipo = 'Despesa'` e registros ordenados com `ORDER BY data`. Tambem
mostra um `JOIN` entre lancamentos e setores. Os comandos correspondentes
estao no arquivo SQL. Salve prints das consultas e dos resultados no SQLTools.

### Update

O script consulta o lancamento antes, atualiza somente a linha identificada
pela descricao e consulta novamente depois do `commit`.

```sql
UPDATE financeiro
SET valor = %s
WHERE descricao = %s
RETURNING id, descricao, valor;
```

No SQLTools, execute primeiro o `SELECT` indicado na secao UPDATE de
`postgresql/02.session.sql` e tire o print de antes. Execute o `UPDATE`, confirme a
transacao (botao de commit, se o auto-commit estiver desligado) e tire o print
depois.

### Delete

O script exibe a linha antes, exclui apenas a descricao escolhida e confirma
com `commit`; a consulta posterior mostra que ela nao existe mais.

```sql
DELETE FROM financeiro
WHERE descricao = %s
RETURNING id, descricao, valor;
```

No SQLTools, tire o print de antes do `DELETE` e outro depois da confirmacao,
executando o `SELECT` posterior para mostrar que a linha foi removida.

## Explicacao da equipe (escrever sem IA)

Esta parte deve ser redigida pela equipe, com pelo menos 15 linhas e com as
proprias palavras. Nao entreguem estes lembretes como se fossem a explicacao:
usem-nos para escrever um relato fiel ao que fizeram e ao codigo:

1. Como configuraram a conexao.
2. Qual biblioteca Python escolheram e por que.
3. Qual comando executaram para conectar.
4. O que representa o objeto de conexao.
5. O que e o cursor e qual foi seu papel.
6. Como o script executou os comandos SQL.
7. Como os parametros foram enviados ao banco.
8. Como os IDs foram gerados.
9. Por que `financeiro` tem uma chave estrangeira.
10. O que as consultas de leitura retornaram.
11. Para que serviu o filtro `WHERE`.
12. Para que serviu a ordenacao `ORDER BY`.
13. Por que o `UPDATE` usou uma condicao `WHERE`.
14. Por que o `DELETE` usou uma condicao `WHERE`.
15. O que `commit` confirma no banco.
16. Como verificaram o resultado no SQLTools.
17. Como o script fecha cursor e conexao.

Completem tambem com as dificuldades que realmente ocorreram:

| Dificuldade e mensagem de erro (texto exato) | Como a equipe resolveu |
| --- | --- |
| Preencher com uma dificuldade real ou escrever “Nao tivemos erros” se for verdade. | Descrever a solucao realmente aplicada. |

## Prints e diario de IA

Incluam no documento final prints legiveis do SQLTools e do terminal: conexao,
estrutura das tabelas, Create, leituras, Update antes/depois e Delete
antes/depois. Os prints devem mostrar os dados/resultados, mas nao a senha,
`.env` ou qualquer outro segredo. Os prints precisam ser feitos pela equipe no
ambiente do banco; este repositorio nao contem imagens de uma conexao real.

Diario de IA: a IA foi usada para ajudar a adaptar o SQL existente, montar o
script Python e organizar este roteiro. A equipe deve acrescentar a data, as
perguntas/prompts que usou e o que revisou ou alterou, de acordo com o uso real.
