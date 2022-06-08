import mysql.connector
import random
import timeit


def conecta():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="certificados"
    )
    cursor = conn.cursor()

    return cursor, conn


def select_id(query, cursor):
    cursor.execute(query)

    myresult = cursor.fetchall()
    id = []

    for x in myresult:
        id.append(x)

    return id


def select_one(array):
    id_one = random.choice(array)
    result = str(id_one).replace("(", "").replace(")", "").replace(",", "")

    return result


def insert(cursor, conn):
    participante_id = select_id('SELECT id from participante', cursor)
    evento_id = select_id(
        'SELECT distinct evento.id from evento JOIN atividade ON evento.id = atividade.evento_id', cursor)
    tipo_atividade_id = select_id('SELECT id from tipo_atividade', cursor)

    funcao_id = select_id('SELECT id from funcao', cursor)
    id_evento = []

    for i in range(len(participante_id)):

        for j in range(5):
            evento = select_one(evento_id)

            teste_id = select_id(
                f'SELECT atividade.id FROM atividade JOIN evento ON evento.id = atividade.evento_id WHERE evento.id = {evento}', cursor)

            tipo_atividade = select_one(tipo_atividade_id)
            atividade = select_one(teste_id)
            funcao = select_one(funcao_id)
            participante = str(participante_id[i]).replace(
                "(", "").replace(")", "").replace(",", "")

            id_evento.append((
                evento,
                tipo_atividade,
                atividade,
                participante,
                funcao,
                '2017-11-27 00:00:00',
                '2017-11-27 00:00:00',
                1,
                '2018-02-21 10:12:26',
                'C16E1AFFFF8AE96F',
                None,
                None,
                None,
                '2018-02-04 21:18:21'
            ))

    query = """ INSERT IGNORE INTO participacao (
        `evento_id`,
        `tipo_atividade_id`,
        `atividade_id`,
        `participante_id`,
        `funcao_id`,
        `data_inicio`,
        `data_fim`,
        `carga_horaria`,
        `data_ultima_emissao`,
        `chave_validacao`,
        `qtd_bolsista`,
        `email_enviado_em`,
        `ordem_autoria`,
        `cadastrado_em`)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
    """
    try:
        cursor.executemany(query, id_evento)
        conn.commit()

    except Exception as e:
        print(e)


inicio = timeit.default_timer()
cursor, conn = conecta()
insert(cursor, conn)
fim = timeit.default_timer()
print(cursor.rowcount, "registos inseridos.")
print('duracao: %f' % (fim - inicio))
