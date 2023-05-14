from flask import Flask, render_template, request
from flask_mysqldb import MySQL


# AQUI SE CONECTA A LA BASE DE DATOS
app = Flask(__name__)
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_PORT"] = 3307
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "mysqlApellido"
mysql = MySQL(app)


# AQUI INICIAN LAS RUTAS DEL NAVEGADOR
@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor() # Es para saber donde está la conexion
        cur.execute('INSERT INTO ... ()')
        return 'recibido'




@app.route('/edit')
def edit_contact():
    return 'edit contact'


@app.route('/delete')
def delete_contact():
    return 'delete contact'


if __name__ == '__main__':
    app.run()

