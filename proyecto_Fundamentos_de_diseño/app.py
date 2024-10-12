from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos
def connect_db():
    return sqlite3.connect('inventario.db')

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para agregar un nuevo cómic
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_comic():
    if request.method == 'POST':
        nombre = request.form['nombre']
        autor = request.form['autor']
        stock = request.form['stock']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO comics (nombre, autor, stock) VALUES (?, ?, ?)', (nombre, autor, stock))
        conn.commit()
        conn.close()
        
        return redirect(url_for('mostrar_inventario'))

    return render_template('agregar_comic.html')

# Ruta para mostrar el inventario de cómics
@app.route('/inventario')
def mostrar_inventario():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comics')
    comics = cursor.fetchall()
    conn.close()
    
    return render_template('mostrar_inventario.html', comics=comics)

# Ruta para eliminar un cómic
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_comic(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM comics WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('mostrar_inventario'))

if __name__ == '__main__':
    # Crear la base de datos si no existe
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            autor TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
    app.run(debug=True)
