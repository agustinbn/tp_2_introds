import csv
import os
from datetime import datetime

ARCHIVO_CSV = 'db/tareas.csv'
CAMPOS = ['id', 'titulo', 'descripcion', 'completada', 'created_at']


def _inicializar_archivo():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CAMPOS)
            writer.writeheader()


def obtener_todas(completada=None, created_at=None):
    _inicializar_archivo()
    tareas = []

    with open(ARCHIVO_CSV, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for fila in reader:
            fila['id'] = int(fila['id'])
            fila['completada'] = fila['completada'] == 'True'
            tareas.append(fila)

    if completada is not None:
        tareas = [t for t in tareas if t['completada'] == completada]

    if created_at is not None:
        tareas = [t for t in tareas if t['created_at'].startswith(created_at)]

    return tareas

def _guardar_todas(tareas):
    with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=CAMPOS)
        writer.writeheader()
        for tarea in tareas:
            writer.writerow(tarea)

def obtener_por_id(tarea_id):
    tareas = obtener_todas()

    for tarea in tareas:
        if tarea['id'] == tarea_id:
            return tarea
        
    return None

def crear(titulo, descripcion):
    """Crea una tarea con descripción y fecha automática."""
    tareas = obtener_todas()

    nuevo_id = 1 if not tareas else max(t['id'] for t in tareas) + 1

    nueva_tarea = {
        'id': nuevo_id, 
        'titulo': titulo, 
        'descripcion': descripcion,
        'completada': False,
        'created_at': datetime.now().isoformat()
    }

    tareas.append(nueva_tarea)
    _guardar_todas(tareas)

    return nueva_tarea

def actualizar(tarea_id, titulo=None, descripcion=None, completada=None):
    tareas = obtener_todas()
    tarea_modificada = None

    for tarea in tareas:
        if tarea['id'] == tarea_id:
            if titulo is not None:
                tarea['titulo'] = titulo
            if descripcion is not None:
                tarea['descripcion'] = descripcion
            if completada is not None:
                tarea['completada'] = completada
            tarea_modificada = tarea
            break

    if tarea_modificada:
        _guardar_todas(tareas)

    return tarea_modificada

def eliminar(tarea_id):
    tareas = obtener_todas()
    tareas_filtradas = [t for t in tareas if t['id'] != tarea_id]

    if len(tareas) != len(tareas_filtradas):
        _guardar_todas(tareas_filtradas)
        return True
    
    return False
