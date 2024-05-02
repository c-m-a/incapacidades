# App Incapacidades

## Instalación

## Requisitos previos
- Python 3 instalado en tu sistema
- Gestor de paquetes Pip instalado
- Git instalado en tu sistema

## Pasos de Instalación

1. Clona el repositorio de GitHub:

    ```bash
    git clone git@github.com:c-m-a/incapacidades.git
    ```

    Reemplaza `<repository_url>` con la URL de tu repositorio de GitHub.

2. Navega al directorio del proyecto:

    ```bash
    cd <repository_name>
    ```

    Reemplaza `<repository_name>` con el nombre del directorio creado después de clonar.

3. (Opcional) Configura un entorno virtual:

    ```bash
    python3 -m venv myenv
    ```

    ```bash
    source myenv/bin/activate   # En Unix/macOS
    ```

    ```bash
    myenv\Scripts\activate      # En Windows
    ```

    Este paso se recomienda para aislar las dependencias de tu proyecto.

4. Instala las dependencias usando pip:

    ```bash
    pip install -r requirements.txt
    ```

    Este comando instala todos los paquetes de Python necesarios especificados en el archivo `requirements.txt`.

5. Realiza las migraciones iniciales de la base de datos:

    ```bash
    python manage.py migrate
    ```

    Este comando configura el esquema inicial de la base de datos.

6. (Opcional) Crea una cuenta de superusuario (admin):

    ```bash
    python manage.py createsuperuser
    ```

    Sigue las instrucciones para crear una cuenta de administrador para acceder a la interfaz de administración de Django.

7. Inicia el servidor de desarrollo:

    ```bash
    python manage.py runserver
    ```

    Este comando inicia el servidor de desarrollo. Puedes acceder a tu aplicación en `http://127.0.0.1:8000/`.

8. (Opcional) Accede a la interfaz de administración de Django:

    Navega a `http://127.0.0.1:8000/admin/` en tu navegador web e inicia sesión con las credenciales de superusuario creadas anteriormente.

9. ¡Listo! Ahora puedes comenzar a desarrollar tu aplicación Django.


