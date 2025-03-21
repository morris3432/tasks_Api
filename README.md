# Tasks API

Una API para gestionar tareas de manera fácil, creada con FastAPI y MySQL como base de datos y cuenta con autetificación OAuth2 y JWT. Esta API incluye Docker para facilitar el despliegue.

## Instalación

> [!NOTE]
> Crea un entorno virtual para evitar problemas de versiones en tu sistema
Antes de todo, necesitas unas librerías las cuales son:
```bash
pip install invoke rich python-dotenv
```

luego ejecuta:
```bash
inv install
```

## Invoke
Esta API cuenta con Invoke, una librería de Python que nos ayuda con tareas repetitivas, similar a Yarn y npm de JavaScript.

En la siguiente tabla se te mostrarán los comandos que tiene el proyecto.

| Titulo | Descripcón | Comandos |
|----------|----------|----------|
| Dev    | Ejecuta el proyecto en modo desarrollo   | inv dev  |
| Run  | Ejecuta el proyecto en modo producción  | inv run |
| Lint   |  Ejecuta linters que ayudan a detectar posibles errores en el código. | inv lint |
| Format | Formatea el código dejando 2 espacios de indentación | inv format |
| Requirements | Actualiza las dependecias de requirements.txt | inv requirements |
| Install | Instala las dependecias de requirements.txt | inv install |

## Docker
### Instrucciones

1. Construye la imagen de Docker: `docker build -t mi-proyecto .`
2. Ejecuta la aplicación: `docker run -p 8000:8000 mi-proyecto`

### Comandos de Docker

* `docker build -t mi-proyecto .`: Construye la imagen de Docker.
* `docker run -p 8000:8000 mi-proyecto`: Ejecuta la aplicación.
* `docker ps`: Muestra los contenedores en ejecución.
* `docker stop <id_contenedor>`: Detiene un contenedor en ejecución.


## Autor

- [@morris3432](https://github.com/morris3432)
