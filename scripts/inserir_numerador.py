import psycopg2


conn = psycopg2.connect(
    dbname = "numerador_crimes",        
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM numerador_categorias")
resultado = cursor.fetchall()

cursor.execute("SELECT * FROM numerador_unidades")
resultado_unidades = cursor.fetchall()

contagem = 0

is_activate = True

for unidade in resultado_unidades:
    for modelo in resultado:
        cursor.execute("""INSERT INTO numerador_numeradores (unidade_id,categoria_id,contagem,is_activate)
                          VALUES (%s,%s,%s,%s)""",(unidade[0],modelo[0],contagem,is_activate))
        conn.commit()
        print("Dados inseridos com sucesso.")