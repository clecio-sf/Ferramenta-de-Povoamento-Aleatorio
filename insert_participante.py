import mysql.connector
import timeit
from faker import Faker

fake = Faker(['pt_BR', 'pt_PT', 'en_US'])


def conecta():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="certificados"
    )
    cursor = conn.cursor()

    return cursor, conn


def generateCpf(i):
    stringConverted = str(i)

    cpfGenerated = stringConverted.zfill(11)

    return cpfGenerated


def insert():

    cursor, conn = conecta()

    insert_db = []
    for i in range(100_000):
        nome = f'{fake.first_name()} {fake.last_name()} {fake.last_name()}'

        insert_db.append((
            generateCpf(i),
            nome,
            '2017-12-23',
            'random-email@hotmail.com',
            None,
            'Sim',
            '2018-02-04 20:43:02'))

    query = """ INSERT INTO participante (
        CPF, nome_completo, data_nascimento, email, email_valido, instituicao_ifba_vca, cadastrado_em)
        VALUES (%s,%s,%s,%s,%s,%s,%s) 
    """

    cursor.execute('SET foreign_key_checks = 0')
    try:
        cursor.executemany(query, insert_db)
        conn.commit()
        print(cursor.rowcount, "registos inseridos.")

    except Exception as e:
        print(e)


inicio = timeit.default_timer()
insert()
fim = timeit.default_timer()
print('duracao da inserção: %f' % (fim - inicio))
