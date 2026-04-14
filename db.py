import mysql.connector


def get_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="prode"
    )


def crear_usuario(nombre, email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)",
        (nombre, email),
    )
    db.commit()
    cursor.close()


def obtener_usuarios():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return usuarios


def buscar_usuario(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    return usuario


def actualizar_usuario(id, nombre, email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s",
        (nombre, email, id),
    )
    db.commit()
    cursor.close()


def eliminar_usuario(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    db.commit()
    cursor.close()


def obtener_partidos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM partidos")
    partidos = cursor.fetchall()
    cursor.close()
    return partidos


def buscar_partido(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM partidos WHERE id = %s", (id,))
    partido = cursor.fetchone()
    cursor.close()
    return partido


def crear_partido(local, visitante, fase, fecha):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO partidos (local, visitante, fase, fecha) VALUES (%s, %s, %s, %s)",
        (local, visitante, fase, fecha),
    )
    db.commit()
    cursor.close()


def actualizar_partido(id, local, visitante, fase, fecha):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE partidos SET local = %s, visitante = %s, fase = %s, fecha = %s WHERE id = %s",
        (local, visitante, fase, fecha, id),
    )
    db.commit()
    cursor.close()


# def modificar_partido(id, data):
#     return id, data


def eliminar_partido(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM partidos WHERE id = %s", (id,))
    db.commit()
    cursor.close()


def actualizar_resultado(id, resultado):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE partidos SET resultado = %s WHERE id = %s", (resultado, id))
    db.commit()
    cursor.close()


def buscar_predicciones_por_usuario(id_usuario):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM predicciones WHERE id_usuario = %s", (id_usuario,))
    predicciones = cursor.fetchall()
    cursor.close()
    return predicciones


def crear_prediccion(id_usuario, id_partido, goles_local, goles_visitante):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO predicciones (id_usuario, id_partido, local, visitante) VALUES (%s, %s, %s, %s)",
        (id_usuario, id_partido, goles_local, goles_visitante),
    )
    db.commit()
    cursor.close()
