from collections import deque
from datetime import datetime
import re

from cli.menu import show_menu
from utils.hightlight import highlight
from core.dispatcher import IncidentDispatcher
from incident.models import Incident
from persistence.storage import IncidentStorage
from rules.incident_rules import incident_rules


def exit_program() -> None:
    print("\nHasta pronto 👋")
    exit()


def default_action() -> None:
    print(highlight("Acción no implementada", "red", True))


def register_incident(dispatcher: IncidentDispatcher, storage: IncidentStorage) -> None:
    """Register a new incident"""
    incident_type = input(
        "Tipo (infrastructure/security/application): ").strip()
    if incident_type not in incident_rules:
        print(highlight("Tipo de incidente no válido", "red", True))
        return

    priority = input("Prioridad (high/medium/low): ").strip()
    if priority not in ["high", "medium", "low"]:
        print(highlight("Prioridad no válida", "red", True))
        return

    description = input("Descripción: ").strip()
    if not description:
        print(highlight("Descripción no puede estar vacía", "red", True))
        return

    incident = Incident(
        id=len(dispatcher.all_incidents) + 1,
        type=incident_type,
        priority=priority,
        description=description,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        assigned_to="",
        status="pending"
    )
    dispatcher.register_incident(incident)
    storage.save_incidents([incident])
    print(
        highlight(f"Incidente registrado con ID: {incident.id}", "green", True))


def show_pending_incidents(dispatcher: IncidentDispatcher) -> None:
    """Show pending incidents"""
    if not dispatcher.pending_queue:
        print(highlight("No hay incidentes pendientes", "yellow", True))
        return

    print(highlight("\nIncidentes Pendientes:", "white", True))
    for incident in dispatcher.pending_queue:
        print(f"[{incident.id}] {incident.type} | Prioridad: {incident.priority} | "
              f"Estado: {incident.status}")


def assign_incident(dispatcher: IncidentDispatcher, storage: IncidentStorage) -> None:
    """Assign an incident to an operator"""
    try:
        incident_id = int(input("ID del incidente: ").strip())
        operator = input("Operador: ").strip()

        if not operator:
            print(highlight("Operador no puede estar vacío", "red", True))
            return

        if operator not in list(dispatcher.operators):
            print(highlight("Operador no registrado", "red", True))
            return

        print(incident_id, operator)
        incident = dispatcher.assign_incident(incident_id, operator)
        if incident:
            all = list(filter(lambda i: i.id != incident_id,
                       dispatcher.all_incidents))
            all.append(incident)
            dispatcher.all_incidents = all
            storage.save_incidents(all)
            print(
                highlight(f"Incidente {incident_id} asignado a {operator}", "green", True))
        else:
            print(highlight("Incidente no encontrado o ya asignado", "red", True))
    except ValueError as e:
        print(highlight(f"ID inválido: {e}", "red", True))
        print(highlight("ID inválido", "red", True))


def resolve_incident(dispatcher: IncidentDispatcher, storage: IncidentStorage) -> None:
    """Resolve an incident"""
    try:
        incident_id = int(input("ID del incidente: ").strip())
        incident = dispatcher.resolve_incident(incident_id)
        if incident:
            all = list(filter(lambda i: i.id != incident_id,
                       dispatcher.all_incidents))
            all.append(incident)
            dispatcher.all_incidents = all
            storage.save_incidents(all)
            print(
                highlight(f"Incidente {incident_id} resuelto", "green", True))
        else:
            print(highlight("Incidente no encontrado o no asignado", "red", True))
    except ValueError:
        print(highlight("ID inválido", "red", True))


def show_history(dispatcher: IncidentDispatcher) -> None:
    """Show resolved/escalated incidents history"""
    if not dispatcher.all_incidents:
        print(highlight("No hay incidentes en el historial", "yellow", True))
        return

    print(highlight("\nHistorial de Incidentes:", "white", True))
    for incident in dispatcher.all_incidents:
        print(f"[{incident.id}] {incident.type} | Prioridad: {incident.priority} | "
              f"Estado: {incident.status} | Asignado a: {incident.assigned_to}")


def search_incidents(dispatcher: IncidentDispatcher) -> None:
    """Search incidents by text, type, operator, or date range"""
    search_type = input("Buscar por (text/type/operator/date): ").strip()
    if search_type not in ["text", "type", "operator", "date"]:
        print(highlight("seleccione una opción válida", "red", True))
        return
    query = input("Ingrese el término de búsqueda: ").strip()
    pattern = re.compile(query, re.IGNORECASE)

    results = []
    for incident in dispatcher.all_incidents:
        if search_type == "text" and pattern.search(incident.description):
            results.append(incident)
        elif search_type == "type" and pattern.search(incident.type):
            results.append(incident)
        elif search_type == "operator" and pattern.search(incident.assigned_to):
            results.append(incident)
        elif search_type == "date" and pattern.search(incident.created_at):
            results.append(incident)

    if not results:
        print(highlight("No se encontraron incidentes", "yellow", True))
        return

    print(highlight("\nResultados de la búsqueda:", "white", True))
    for incident in results:
        print(f"[{incident.id}] {incident.type} | Prioridad: {incident.priority} | "
              f"Estado: {incident.status} | Asignado a: {incident.assigned_to}")


def main():
    dispatcher = IncidentDispatcher()
    storage = IncidentStorage()
    dispatcher.operators = {"carlos", "maria", "pedro"}  # Example operators
    print(storage.load_incidents())

    dispatcher.pending_queue = deque(filter(
        lambda i: i.status == "pending", storage.load_incidents()))
    dispatcher.in_progress = list(filter(
        lambda i: i.status == "in_progress", storage.load_incidents()))
    dispatcher.history = list(filter(
        lambda i: i.status != "pending", storage.load_incidents()))
    dispatcher.all_incidents = storage.load_incidents()

    while True:
        # os.system("clear")
        print(highlight("\nGestión de Incidentes y Flujos de Escalamiento\n",
              color="white", bold=True))
        show_menu()

        try:
            action = int(input("\n¿Qué deseas hacer? (1-7): ").strip())

            if action == 1:
                register_incident(dispatcher, storage)
            elif action == 2:
                show_pending_incidents(dispatcher)
            elif action == 3:
                assign_incident(dispatcher, storage)
            elif action == 4:
                resolve_incident(dispatcher, storage)
            elif action == 5:
                show_history(dispatcher)
            elif action == 6:
                search_incidents(dispatcher)
            elif action == 7:
                exit_program()
            else:
                default_action()

            # input("\nPresione Enter para continuar...")

        except ValueError:
            default_action()
        except KeyboardInterrupt:
            exit_program()


if __name__ == "__main__":
    main()
