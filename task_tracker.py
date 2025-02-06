import json
import argparse
import os
import uuid
from datetime import datetime

TASKS_FILE = "tasks.json"

# Cargar tareas desde el archivo JSON
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

# Guardar tareas en el archivo JSON
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Agregar una nueva tarea con las propiedades requeridas
def add_task(description):
    tasks = load_tasks()
    new_task = {
        "id": str(uuid.uuid4()),
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Tarea '{description}' agregada con ID {new_task['id']}.")

# Actualizar una tarea por ID
def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Tarea {task_id} actualizada.")
            return
    print("ID de tarea no encontrado.")

# Eliminar una tarea por ID
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Tarea {task_id} eliminada.")

# Cambiar el estado de una tarea por ID
def change_status(task_id, status):
    if status not in ["todo", "in-progress", "done"]:
        print("Estado no válido. Usa: todo, in-progress, done.")
        return

    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Tarea {task_id} marcada como '{status}'.")
            return
    print("ID de tarea no encontrado.")

# Listar tareas según filtro
def list_tasks(status=None):
    tasks = load_tasks()
    filtered_tasks = [task for task in tasks if status is None or task["status"] == status]
    
    if not filtered_tasks:
        print("No hay tareas para mostrar.")
        return

    for task in filtered_tasks:
        print(f"[{task['id']}] {task['description']} - {task['status']} (Creado: {task['createdAt']}, Última actualización: {task['updatedAt']})")

# Configuración de argumentos en la línea de comandos
parser = argparse.ArgumentParser(description="Task Tracker CLI")
parser.add_argument("command", choices=["add", "update", "delete", "status", "list"], help="Acción a realizar")
parser.add_argument("args", nargs="*", help="Argumentos adicionales")

args = parser.parse_args()

# Ejecutar la acción correspondiente
if args.command == "add":
    if not args.args:
        print("Debes proporcionar una descripción para la tarea.")
    else:
        add_task(" ".join(args.args))

elif args.command == "update":
    if len(args.args) < 2:
        print("Debes proporcionar un ID y una nueva descripción.")
    else:
        update_task(args.args[0], " ".join(args.args[1:]))

elif args.command == "delete":
    if not args.args:
        print("Debes proporcionar un ID de tarea.")
    else:
        delete_task(args.args[0])

elif args.command == "status":
    if len(args.args) < 2:
        print("Debes proporcionar un ID y un estado (todo, in-progress, done).")
    else:
        change_status(args.args[0], args.args[1])

elif args.command == "list":
    status_filter = args.args[0] if args.args else None
    list_tasks(status_filter)
