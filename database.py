import sqlite3

# Crear una conexión a la base de datos SQLite
conn = sqlite3.connect('mantenimiento_dbs.sqlite')
cursor = conn.cursor()

# Crear las tablas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Equipos (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    estado TEXT NOT NULL,
    fecha_adquisicion DATE NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Mantenimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipo_id TEXT,
    fecha_mantenimiento DATE NOT NULL,
    descripcion TEXT NOT NULL,
    costo REAL NOT NULL,
    FOREIGN KEY (equipo_id) REFERENCES Equipos(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefono TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS UsuariosEquipos (
    usuario_id INTEGER,
    equipo_id TEXT,
    PRIMARY KEY (usuario_id, equipo_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id),
    FOREIGN KEY (equipo_id) REFERENCES Equipos(id)
);
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos y tablas creadas con éxito.")