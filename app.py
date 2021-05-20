from flask import *
import psycopg2
import pymysql

app = Flask(__name__)

connection = pymysql.connect(host='localhost',
                             user='admin',
                             password='admin',
                             database='admin',
                             cursorclass=pymysql.cursors.DictCursor)

cursor_mysql = connection.cursor()

#---------------------CONEXAO COM O BANCO DE DADOS POSTGRESQL-----------------------------

conn = psycopg2.connect(dbname="admin",
                        user="admin",
                        password="admin")
cursor_pg = conn.cursor()



@app.route("/api/macapa", methods=['POST'])
def api_macapa():

    #   COLEÇÂO DE DADOS
    data = request.get_json()

    contacts = list(data['contacts'])

    for lista in contacts:
        name = (lista['name']).upper()
        cellphone = (lista['cellphone']).upper()

        mask = (f'+{cellphone[:2]} ({cellphone[2:4]}) {cellphone[4:8]}-{cellphone[8:]}')

        cursor_mysql.execute(f"""INSERT INTO `admin`.`contacts` (`nome`, `celular`) VALUES ('{name}', '{mask}');""")
        connection.commit()

    return ('ok'),200



@app.route("/api/varejao", methods=['POST'])
def api_varejao():

    #   COLEÇÂO DE DADOS
    data = request.get_json()

    contacts = list(data['contacts'])

    for lista in contacts:
        name = lista['name']
        cellphone = lista['cellphone']

        cursor_pg.execute(f"""INSERT INTO "public"."contacts" ("nome", "celular") VALUES ('{name}', '{cellphone}');""")
        conn.commit()

    return ('ok'),200



if __name__ == '__main__':
  app.run(debug=True)