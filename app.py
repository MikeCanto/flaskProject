from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

# AQUI SE CONECTA A LA BASE DE DATOS
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_PORT"] = 3307
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "mysqlApellido"
mysql = MySQL(app)

# Configuraciones
app.secret_key = 'mysecretkey'


# AQUI INICIAN LAS RUTAS DEL NAVEGADOR
@app.route('/')
def Index():  # put application's code here
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos')
    data = cur.fetchall()  # Se obtienen todos los alumnos con sus datos
    flash('Reprobados: ' + reprobados())
    return render_template('index.html', alumnos=data)  # Se envian a "index.html"

def reprobados():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos')
    lista = cur.fetchall()
    print('Total rows are: ' ,len(lista))
    nreprobados = 0
    for row in lista:
        if row[4] < 60:
            nreprobados += 1
    return str(nreprobados)




@app.route('/add_contact', methods=['POST'])
def add_contact():  # El boton de envio llama a este metodo
    if request.method == 'POST':
        id_alu = request.form['id_alu']
        nombre_alu = request.form['nombre_alu']
        ape_p_alu = request.form['ape_p_alu']
        ape_m_alu = request.form['ape_m_alu']
        promedio = request.form['promedio']
        cur = mysql.connection.cursor()  # Es para saber donde está la conexion
        cur.execute(
            'INSERT INTO alumnos(id_alu, nombre_alu, ape_p_alu, ape_m_alu, promedio) VALUES (%s, %s, %s, %s, %s)',
            (id_alu, nombre_alu, ape_p_alu, ape_m_alu, promedio))
        mysql.connection.commit()  # Se envia el query
        flash('Alumno agregado')  # Envia mensaje index.html
        return redirect(url_for('Index'))  # Te regresa al metodo Index -> "index.html"


@app.route('/edit/<id_alu>')
def get_alumno(id_alu):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos WHERE id_alu = {0}'.format(id_alu))
    data = cur.fetchall()  # Se obtienen los datos del alumno
    return render_template('edit-alumno.html', alumno=data[0])  # Se envian los datos del alumno a "edit-alumno.html"


@app.route('/update/<id_alu>', methods=['POST'])
def update_alumno(id_alu):
    if request.method == 'POST':
        nombre_alu = request.form['nombre_alu']  # Se reciben los datos del "edit_alumno.html"
        ape_p_alu = request.form['ape_p_alu']
        ape_m_alu = request.form['ape_m_alu']
        promedio = request.form['promedio']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE alumnos
            SET nombre_alu = %s,
                ape_p_alu = %s,
                ape_m_alu = %s,
                promedio = %s
            WHERE id_alu = %s 
        """, (nombre_alu, ape_p_alu, ape_m_alu, promedio, id_alu))  # Se envia la query para actualizar
        mysql.connection.commit()  # Se comitea
        flash('Alumno actualizado')
        return redirect(url_for('Index'))


@app.route('/delete/<string:id_alu>')
def delete_contact(id_alu):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM alumnos WHERE id_alu = {0}'.format(id_alu))
    mysql.connection.commit()
    flash('Contacto eliminado')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run()
