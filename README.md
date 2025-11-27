# Sistema de Registro y Seguimiento de Solicitudes

En este proyecto desarrollé una aplicación web sencilla para **registrar, consultar y dar seguimiento** a solicitudes internas.  
La idea es dejar de usar hojas de cálculo o mensajes sueltos y tener todo en un solo lugar.

Este sistema fue realizado como **proyecto final** de la materia *Administración del Proceso de Software*.

---

## Objetivo del proyecto

Construir una aplicación web que permita:

- Crear solicitudes con datos básicos.
- Ver un listado general de solicitudes.
- Editar y eliminar registros.
- Filtrar la información.
- Exportar el listado a un archivo CSV como reporte simple.

---

## Funcionalidades principales

- **Alta de solicitudes**  
  Campos: folio, fecha, solicitante, tipo, estado y descripción (opcional).

- **Listado de solicitudes**  
  Tabla con todas las solicitudes registradas.

- **Filtros**  
  - Por estado  
  - Por tipo  
  - Por texto (folio, solicitante o descripción)

- **Edición de solicitudes**  
  Actualizar datos cuando cambie el estado o la información.

- **Eliminación de solicitudes**  
  Borrar solicitudes que ya no se necesiten.

- **Exportación a CSV**  
  Generar un archivo CSV con las solicitudes visibles en la tabla.

---

## Tecnologías utilizadas

- **Backend:** Python 3 + Flask  
- **Base de datos:** SQLite  
- **Frontend:** HTML, CSS, Bootstrap básico  
- **Control de versiones:** Git y GitHub

---

## Requisitos

- Python 3 instalado
- `pip` instalado

---

## Cómo ejecutar el proyecto

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/usuario/proyecto-solicitudes.git
   cd Proyecto_Final
   
