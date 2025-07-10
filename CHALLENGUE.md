# 🧠 Proyecto Final 1: Simulador de Gestión de Incidentes y Flujos de Escalamiento

## 📘 Contexto/Introducción
Imagina un centro de operaciones de una empresa donde los usuarios reportan incidentes: desde caídas del sistema, fallas de red, hasta alertas de seguridad. Cada incidente debe ser registrado, categorizado, priorizado y escalado automáticamente de acuerdo a reglas dinámicas. Este proyecto emula la lógica interna de un centro de gestión de incidentes (SOC/NOC) con cola de atención, historial, y reglas de escalamiento basadas en tiempo, prioridad o categoría.

Esto es lo más parecido a un backend real sin usar base de datos.

## ✅ Requerimientos Funcionales

🧾 Estructura de un incidente (Incident)

Usa `@dataclass(frozen=True)`:
```python
@dataclass(frozen=True)
class Incident:
    id: int
    type: str  # e.g., "infrastructure", "security", "application"
    priority: str  # "high", "medium", "low"
    description: str
    created_at: datetime
    assigned_to: Optional[str]
    status: str  # "pending", "in_progress", "resolved", "escalated"
```

## 🧠 Reglas de negocio (core logic)
- Un incidente puede escalar automáticamente si no ha sido atendido en N minutos (usando datetime.now()).

- Solo ciertos roles pueden resolver ciertos tipos de incidente.

- Si un incidente es prioridad alta, entra al inicio de la cola.

- El sistema debe poder filtrar y despachar incidentes automáticamente a operadores disponibles.

## 🧱 Estructuras necesarias
- Queue de incidentes por prioridad.

- Set de operadores disponibles.

- Dict de reglas: tipo → roles permitidos.

- List con historial (resolved, escalated, etc.).

## 🖥️ Funcionalidades
- Registrar un nuevo incidente.

- Mostrar incidentes pendientes por prioridad.

- Asignar un incidente a un operador válido.

- Resolver un incidente.

- Escalar automáticamente incidentes según condiciones (tiempo/prioridad).

- Ver historial de incidentes resueltos/escalados.

- Guardar todos los incidentes en .json al cerrar.

- Buscar incidentes por texto, tipo, operador, rango de fechas (regex + datetime).

## 🧠 Complejidad técnica requerida
| Tema                                                     | Aplicación esperada                                                            |
| -------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `dataclasses`, `slots`                                   | Incidentes, operadores                                                         |
| `typing`, `collections`                                  | `Deque`, `DefaultDict`, `TypedDict`, `Union`, `Optional`, `Literal`            |
| `regex-II`, `datetime`, `json`                           | Búsqueda avanzada, vencimientos                                                |
| `closures`, `decorators`, `contextmanager`               | Control de sesiones, logs, validaciones                                        |
| `generators`, `iterators`                                | Iterar incidentes por estado, o crear filtros perezosos                        |
| `abstraction`, `composition`, `SRP`, `LSP`, `ISP`, `DIP` | Separación clara de lógica, estrategia de escalamiento como función inyectada  |
| `modules`                                                | Estructura en paquetes: `incident/`, `core/`, `cli/`, `persistence/`, `rules/` |


## 📦 Ejemplo de arquitectura sugerida
```
incident_manager/
├── main.py
├── core/
│   ├── dispatcher.py
│   ├── escalator.py
│   └── validator.py
├── incident/
│   ├── models.py
│   └── filters.py
├── rules/
│   └── default_rules.py
├── persistence/
│   └── storage.py
├── cli/
│   └── interface.py
└── logs/
    └── events.log
```

## 🧾 Entrada/salida simulada
```
    > Registrar incidente
    Tipo: infraestructura
    Prioridad: alta
    Descripción: caída de servidores de autenticación
    ✔ ID generado: 001

    > Ver incidentes pendientes (3)
    [001] Infraestructura | Prioridad: alta | Estado: pendiente

    > Asignar incidente 001 a operador "carlos"
    ✔ Asignado correctamente.

    > Resolver incidente 001
    ✔ Marcado como resuelto

    > Ver historial
    [001] Resuelto por carlos a las 2025-05-06 19:13:21
```
