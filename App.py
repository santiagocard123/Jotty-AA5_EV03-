from flask import Flask, request, jsonify
import sqlite3
import uuid

app = Flask(__name__)
DATABASE = 'mantenimiento_dbs.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/equipos', methods=['POST'])
def crear_equipo():
    data = request.get_json()  
    
    if not all(key in data for key in ('nombre', 'marca', 'modelo', 'estado', 'fecha_adquisicion')):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    nombre = data['nombre']
    marca = data['marca']
    modelo = data['modelo']
    estado = data['estado']
    fecha_adquisicion = data['fecha_adquisicion']
    
    equipo_id = str(uuid.uuid4())
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Equipos (id, nombre, marca, modelo, estado, fecha_adquisicion)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (equipo_id, nombre, marca, modelo, estado, fecha_adquisicion))
    conn.commit()
    conn.close()
    
    return jsonify({'id': equipo_id}), 201

@app.route('/equipos', methods=['GET'])
def obtener_equipos():
    conn = get_db_connection()
    equipos = conn.execute('SELECT * FROM Equipos').fetchall()
    conn.close()
    
    return jsonify([dict(equipo) for equipo in equipos])

@app.route('/equipos/<id>', methods=['GET'])
def obtener_equipo_por_id(id):
    conn = get_db_connection()
    equipo = conn.execute('SELECT * FROM Equipos WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if equipo:
        return jsonify(dict(equipo))
    else:
        return jsonify({'error': 'Equipo no encontrado'}), 404

@app.route('/equipos/<id>', methods=['PUT'])
def actualizar_equipo(id):
    data = request.get_json()
    
    if not all(key in data for key in ('nombre', 'marca', 'modelo', 'estado', 'fecha_adquisicion')):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    nombre = data['nombre']
    marca = data['marca']
    modelo = data['modelo']
    estado = data['estado']
    fecha_adquisicion = data['fecha_adquisicion']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Equipos
        SET nombre = ?, marca = ?, modelo = ?, estado = ?, fecha_adquisicion = ?
        WHERE id = ?
    ''', (nombre, marca, modelo, estado, fecha_adquisicion, id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Equipo actualizado con éxito.'})

@app.route('/equipos/<id>', methods=['DELETE'])
def eliminar_equipo(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Equipos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Equipo eliminado con éxito.'})

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    
    if not all(key in data for key in ('nombre', 'email', 'telefono')):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    nombre = data['nombre']
    email = data['email']
    telefono = data['telefono']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Usuarios (nombre, email, telefono)
        VALUES (?, ?, ?)
    ''', (nombre, email, telefono))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Usuario creado con éxito.'}), 201

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM Usuarios').fetchall()
    conn.close()
    
    return jsonify([dict(usuario) for usuario in usuarios])

@app.route('/usuarios/<id>', methods=['GET'])
def obtener_usuario_por_id(id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM Usuarios WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if usuario:
        return jsonify(dict(usuario))
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

@app.route('/usuarios/<id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.get_json()
    
    if not all(key in data for key in ('nombre', 'email', 'telefono')):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    nombre = data['nombre']
    email = data['email']
    telefono = data['telefono']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Usuarios
        SET nombre = ?, email = ?, telefono = ?
        WHERE id = ?
    ''', (nombre, email, telefono, id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Usuario actualizado con éxito.'})

@app.route('/usuarios/<id>', methods=['DELETE'])
def eliminar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Usuario eliminado con éxito.'})

@app.route('/mantenimientos', methods=['POST'])
def crear_mantenimiento():
    data = request.get_json()
    
    if not all(key in data for key in ('equipo_id', 'fecha_mantenimiento', 'descripcion', 'costo')):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    equipo_id = data['equipo_id']
    fecha_mantenimiento = data['fecha_mantenimiento']
    descripcion = data['descripcion']
    costo = data['costo']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Mantenimientos (equipo_id, fecha_mantenimiento, descripcion, costo)
        VALUES (?, ?, ?, ?)
    ''', (equipo_id, fecha_mantenimiento, descripcion, costo))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Mantenimiento creado con éxito.'}), 201

@app.route('/mantenimientos', methods=['GET'])
def obtener_mantenimientos():
    conn = get_db_connection()
    mantenimientos = conn.execute('SELECT * FROM Mantenimientos').fetchall()
    conn.close()
    
    return jsonify([dict(mantenimiento) for mantenimiento in mantenimientos])

@app.route('/mantenimientos/<id>', methods=['GET'])
def obtener_mantenimiento_por_id(id):
    conn = get_db_connection()
    mantenimiento = conn.execute('SELECT * FROM Mantenimientos WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if mantenimiento:
        return jsonify(dict(mantenimiento))
    else:
        return jsonify({'error': 'Mantenimiento no encontrado'}), 404

@app.route('/mantenimientos/<id>', methods=['PUT'])
def actualizar_mantenimiento(id):
    data = request.get_json()
    
    if not all(key in data for key in ('equipo_id', 'fecha_mantenimiento', 'descripcion', 'costo')):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    equipo_id = data['equipo_id']
    fecha_mantenimiento = data['fecha_mantenimiento']
    descripcion = data['descripcion']
    costo = data['costo']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Mantenimientos
        SET equipo_id = ?, fecha_mantenimiento = ?, descripcion = ?, costo = ?
        WHERE id = ?
    ''', (equipo_id, fecha_mantenimiento, descripcion, costo, id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Mantenimiento actualizado con éxito.'})

@app.route('/mantenimientos/<id>', methods=['DELETE'])
def eliminar_mantenimiento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Mantenimientos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Mantenimiento eliminado con éxito.'})

@app.route('/usuarios/equipos', methods=['POST'])
def asignar_equipo_a_usuario():
    data = request.get_json()
    
    if not all(key in data for key in ('usuario_id', 'equipo_id')):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    usuario_id = data['usuario_id']
    equipo_id = data['equipo_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO UsuariosEquipos (usuario_id, equipo_id)
        VALUES (?, ?)
    ''', (usuario_id, equipo_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Equipo asignado al usuario con éxito.'}), 201

@app.route('/consulta', methods=['GET'])
def consulta():
    conn = get_db_connection()
    query = '''
        SELECT u.id AS usuario_id, u.nombre AS nombre_usuario, 
               e.id AS equipo_id, e.nombre AS nombre_equipo, 
               e.modelo, e.marca, e.estado
        FROM Usuarios u
        JOIN UsuariosEquipos ue ON u.id = ue.usuario_id
        JOIN Equipos e ON ue.equipo_id = e.id
    '''
    resultados = conn.execute(query).fetchall()
    conn.close()
    
    return jsonify([dict(resultado) for resultado in resultados])

if __name__ == '__main__':
    app.run(debug=True)