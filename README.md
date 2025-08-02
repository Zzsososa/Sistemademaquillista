# Lucero Glam Studio App

Una aplicación web para administrar el negocio de maquillaje Lucero Glam Studio, desarrollada con Python, Streamlit y SQLite.

## Características

- Registro y gestión de clientes
- Interfaz de usuario intuitiva y moderna
- Base de datos SQLite para almacenamiento persistente
- Funcionalidades CRUD completas para clientes

## Requisitos

- Python 3.7 o superior
- Streamlit
- Pandas
- SQLite3 (incluido en Python)

## Instalación

1. Clone este repositorio o descargue los archivos en su computadora.
2. Instale las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Uso

1. Navegue hasta el directorio del proyecto en su terminal.
2. Ejecute la aplicación con Streamlit:

```bash
streamlit run app.py
```

3. La aplicación se abrirá automáticamente en su navegador web predeterminado.

## Estructura del Proyecto

- `app.py`: Archivo principal de la aplicación Streamlit
- `database.py`: Módulo para la gestión de la base de datos SQLite
- `requirements.txt`: Lista de dependencias del proyecto
- `data/`: Directorio donde se almacena la base de datos (se crea automáticamente)

## Funcionalidades

### Gestión de Clientes
- Registrar nuevos clientes con nombre, apellido, número de teléfono y descripción opcional
- Buscar clientes por nombre o número de teléfono
- Editar información de clientes existentes
- Eliminar clientes del sistema

## Próximas Funcionalidades

- Gestión de citas y calendario
- Registro de servicios y precios
- Seguimiento de pagos e ingresos
- Estadísticas y reportes del negocio
