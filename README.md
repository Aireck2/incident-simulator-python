# 🛒 Final Project: Incident management and escalation flow simulator

This is a simple command-line application that simulates the process of incident management and escalation. It allows you to register incidents, view pending incidents, assign incidents to operators, resolve incidents, and view the incident history. The application also provides a search feature to find incidents by text, type, operator, or date range.

<!-- <div style="text-align: center"> -->
<!-- <img src="./assets/demo.gif" alt="Demo of the Shopping Cart Simulator" width="600" style="margin-bottom: 20px;">
</div> -->

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/aireck2/incident-simulator-python.git
```

### 2. (Optional) Create and activate a virtual environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
source venv/bin/activate
```

### 4. Run the application

Simply run:

```bash
python main.py
```

## 💻 Features

- Register incidents: You can register new incidents by entering the type, priority, and description.
- View pending incidents: You can view all pending incidents in the queue.
- Assign incidents to operators: You can assign an incident to an operator by entering the incident ID and the operator's name.
- Resolve incidents: You can resolve an incident by entering the incident ID.
- View incident history: You can view all incidents in the history, including resolved and escalated incidents.
- Search incidents: You can search incidents by text, type, operator, or date range.

- Exit: Exit the program.

## 🧩 Customization

- You can customize the incident types, priorities, and escalation times in the `rules/incident_rules.py` file.
- You can customize the operators allowed to assign incidents in the `main.py` file.
- You can customize the file path for the incident history in the `persistence/storage.py` file.

## 📄 Requirements

- Python 3.7 or higher.

## 👨‍💻 Author

- [Erick Escriba | @Aireck2](https://github.com/Aireck2)

This is an educational project created as part of a final assignment.
