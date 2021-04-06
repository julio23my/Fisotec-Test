import psycopg2
import hashlib


    



PASSWORD='prueba'
conn = psycopg2.connect(
    host="127.0.0.1",
    port='4040',
    database="test",
    user="postgres",
    password="postgres")

cur = conn.cursor()
cur.execute("""SELECT * FROM administracion.usuario""")
for record in cur:
    hashpass = hashlib.md5(PASSWORD.encode('utf8')).hexdigest()
    print(hashpass== record[1])
    


