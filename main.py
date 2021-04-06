"""
This program is performing the tasks indicated in the file
'Ejercicio.pdf'
of Fisotec (https://fisotec.es)
Using: 
    docker: postgresql 10.4 localhost on port (4040), postgis 2.4, db test "if wanna test please change psycopg2.connect params"
    python: 3.7

"""

#Database
import psycopg2

#Decode and encode password
import hashlib

#Datetime
from datetime import datetime


#Constans

PASSWORD='prueba'
USUARIO='prueba'
#List of updated tables
LIST_UPDATE_TABLE=['gestlighting_centro_mando','gestlighting_luminaria','gestlighting_modulo_medida']

def _print_welcome():
    """
    Print the welcome functions
    """
    print('WELCOME TO TEST FISOTEC')
    print('*' * 50)
    print('What would you like to do today?:')
    print('[C]onnect with the data base')
    print('[S]earch a especific ID in a table')
    print(f'[U]pdate the vial column in {LIST_UPDATE_TABLE} ')
    print('[E]xit program')


def connect_defaultuser():
    """
    Connect to database using "usuario, clave" 
    columns and insert session.
    """
    encode = hashlib.md5(PASSWORD.encode('utf8')).hexdigest()
    consult = f"SELECT * FROM administracion.usuario WHERE id_usuario='{USUARIO}' AND clave='{encode}' "
    cur.execute(consult)
    login = cur.fetchall()[0]
    if login:
        print("Is connect to database")
        return session_login(login)
    else:
        print("user or password not correct")


def session_login(login):
    """
    Record session login into data base.
    login: record login to get user data
    """
    consult = f"INSERT INTO administracion.sesion ( usuario, proyecto, inicio) VALUES ( '{login[0]}', '{login[3]}', '{now}') RETURNING id_sesion"
    cur.execute(consult)
    global id_session 
    id_session = cur.fetchone()[0]
    conn.commit()
    

def session_logout():
    """
    Record login session finish in 'fin' database of 'id_session'
    """
    consult = f"UPDATE administracion.sesion SET fin='{now}' WHERE  id_sesion= {id_session} "
    cur.execute(consult)
    conn.commit()
    conn.close()
    print("Logout complete")


def check_sch():
    """
    Validate if the schema exists
    """
    existing = None
    while not existing:
        schema = input("Please insert the schema: ").lower()
        consult = f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema}';"
        cur.execute(consult)
        existing = cur.fetchall()
        if existing:
            return schema
        else:
            print("This schema doesn't exists")
    

def check_table():
    """
    Validate if the table exists
    """
    existing = None
    while not existing:
        table = input("Please insert the table: ").lower()
        session = f"SELECT table_name FROM information_schema.tables WHERE table_name = '{table}';"
        cur.execute(session)
        existing = cur.fetchall()
        if existing:
            return table
        else:
            print("This table doesn't exists")


def print_data_table(schema, table):
    """
    This functions search in database the 'schema' and 'table'
    and get the column id to print a specific row of id
    """
    try:
        cur.execute(f"SELECT * FROM {schema}.{table} ")
        for columns in cur.description:
            if 'id_' in columns[0]:
                column_id = columns[0]
                break
        data_search = input(f"Please insert the id of {column_id}  : ")
        
        cur.execute("SELECT * FROM %s.%s WHERE %s = '%s'" %(schema,table, column_id, data_search))
        existing = cur.fetchall()
        if existing:
           for row in existing:
                print(row)
        else:
            print("This id doesn't exists")
            
    except(Exception, psycopg2.Error) as error:
        print('Error executing SQL command ', error)


def update_vial_values(tables_update):
    """
    This function update the vial field of selectes tables with the closer range in the base_vial
    """
    for table in tables_update:
        try:
            cur.execute("""
            UPDATE alcaudete_desarrollo_gissmart_energy.%s as a
            SET  vial = (
                SELECT b.id_vial 
                FROM   alcaudete_desarrollo_gissmart_energy.base_vial as b
                ORDER BY
                    a.geom <-> b.geom
                LIMIT  1
            )
            
            """ 
            %(table)
            )
            conn.commit()
            print(f"Updated vial of : {table}")
        except(Exception, psycopg2.Error) as error:
            print('Error executing SQL command ', error)

    
if __name__ == '__main__':
    now = datetime.now()

    try:
        conn = psycopg2.connect(host="127.0.0.1",port='4040',database="test",user="postgres",password="postgres")
        cur = conn.cursor()
        cur.execute("SELECT version();")
        record = cur.fetchone()
        print(f"You are connected into the - {record}\n")
        connect_defaultuser()

    except(Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database", error)
        connection = None

    _print_welcome()

    command = input()
    command = command.upper()

    if command == 'C':
        connect_defaultuser()

    elif command == 'S':
        print_data_table(check_sch(), check_table())

    elif command == 'U':
        update_vial_values(LIST_UPDATE_TABLE);

    try:
        session_logout()
        
    except(Exception, psycopg2.Error) as error:
        print('Error codigo finalizado error ', error)