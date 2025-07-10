from typing import TypedDict


class MenuItem(TypedDict):
    id: int
    label: str


menu_list: list[MenuItem] = [
    {
        "id": 1,
        "label": "1. Registrar incidente"
    },
    {
        "id": 2,
        "label": "2. Mostrar incidentes pendientes",
    },
    {
        "id": 3,
        "label": "3. Asignar incidente a operador",
    },
    {
        "id": 4,
        "label": "4. Resolver incidente",
    },
    {
        "id": 5,
        "label": "5. Historial de incidentes resueltos/escalados",
    },
    {
        "id": 6,
        "label": "6. Buscar incidentes por texto, tipo, operador, rango de fechas",
    },
    {
        "id": 7,
        "label": "7. Salir"
    }
]


def show_menu() -> None:
    for item in menu_list:
        print(item.get("label"))
    print("\n")
