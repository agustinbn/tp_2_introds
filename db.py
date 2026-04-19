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


def obtener_partidos(limit, offset,equipo, fase, fecha):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM partidos"
    conditions = []
    datos = []

    if equipo:
        conditions.append("equipo_local = %s OR equipo_visitante = %s")
        datos.append(equipo)
        datos.append(equipo)
    if fase:
        conditions.append("fase = %s")
        datos.append(fase)
    if fecha:
        conditions.append("fecha = %s")
        datos.append(fecha)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id LIMIT %s OFFSET %s"
    datos.extend([limit, offset])

    cursor.execute(query, tuple(datos))
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

def contar_partido(equipo, fase, fecha):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT COUNT(*) as total FROM partidos"
    conditions = []
    datos = []

    if equipo:
        conditions.append("equipo_local = %s OR equipo_visitante = %s")
        datos.append(equipo)
        datos.append(equipo)
    if fase:
        conditions.append("fase = %s")
        datos.append(fase)
    if fecha:
        conditions.append("fecha = %s")
        datos.append(fecha)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, tuple(datos))
    total_registros = cursor.fetchone()[0]
    cursor.close()
    return total_registros

def crear_partido(equipo_local, equipo_visitante, fase, fecha):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO partidos (equipo_local, equipo_visitante, fase, fecha) VALUES (%s, %s, %s, %s)",
        (equipo_local, equipo_visitante, fase, fecha),
    )
    db.commit()
    cursor.close()


def actualizar_partido(id, equipo_local, equipo_visitante, fase, fecha):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE partidos SET equipo_local = %s, equipo_visitante = %s, fase = %s, fecha = %s WHERE id = %s",
        (equipo_local, equipo_visitante, fase, fecha, id),
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

def existe_prediccion( id_usuario, id_partido):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT 1 FROM predicciones WHERE id_usuario = %s AND id_partido = %s",
        (id_usuario, id_partido))

    resultado = cursor.fetchone() is not None
    cursor.close()
    db.close()
    return resultado

def obtener_ranking(limit, offset):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT
        u.id AS id_usuario,
        u.nombre,
        SUM(
            CASE
                -- 3 PUNTOS: Acierto Exacto
                WHEN pr.local = JSON_EXTRACT(pa.resultado, '$.local')
                 AND pr.visitante = JSON_EXTRACT(pa.resultado, '$.visitante') THEN 3

                -- 1 PUNTO: Acierto Tendencia (Ganador o Empate)
                WHEN SIGN(pr.local - pr.visitante) = SIGN(JSON_EXTRACT(pa.resultado, '$.local') - JSON_EXTRACT(pa.resultado, '$.visitante')) THEN 1

                ELSE 0
            END
        ) AS puntos
    FROM usuarios u
    JOIN predicciones pr ON u.id = pr.id_usuario
    JOIN partidos pa ON pr.id_partido = pa.id
    WHERE pa.resultado IS NOT NULL
    GROUP BY u.id
    ORDER BY puntos DESC
    LIMIT %s OFFSET %s
    """

    cursor.execute(query, (limit, offset))
    ranking = cursor.fetchall()
    cursor.close()
    return ranking
