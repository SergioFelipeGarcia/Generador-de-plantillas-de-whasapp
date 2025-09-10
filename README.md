
# 💬 Generador de Plantillas de WhatsApp Pro

---

## ✨ Descripción del Proyecto

"Generador de Plantillas de WhatsApp Pro" es una aplicación creada con Streamlit que utiliza el poder de la inteligencia artificial de Google Gemini para generar plantillas de mensajes optimizadas para WhatsApp Business.

La herramienta ayuda a empresas y profesionales a crear plantillas efectivas, que cumplen con las políticas de WhatsApp y están diseñadas para maximizar la interacción y las conversiones.

## 🚀 Características Principales

* **Generación por IA:** Crea plantillas únicas y profesionales en segundos, basadas en el sector y la audiencia de tu negocio.
* **Cumplimiento de Políticas:** Diseña mensajes que se adhieren estrictamente a las reglas de WhatsApp para evitar rechazos y bloqueos.
* **Vista Previa:** Muestra un *mockup* de cómo se verán las plantillas en un chat de WhatsApp real, incluyendo cabecera, cuerpo y botones.
* **Descarga Fácil:** Permite descargar las plantillas generadas en un archivo de texto simple (`.txt`).
* **Interfaz Intuitiva:** Un formulario sencillo en el que solo debes rellenar los datos de tu negocio para obtener resultados.

## ⚙️ Requisitos y Configuración

Para ejecutar esta aplicación, necesitas tener Python instalado en tu sistema y una clave de API de Google Gemini.

### 1. Requisitos de Python

Instala las bibliotecas necesarias ejecutando el siguiente comando en tu terminal:

```bash
pip install -r requirements.txt
````

> **Nota:** El contenido del archivo `requirements.txt` se encuentra más abajo.

### 2\. Obtener la Clave de API

La aplicación requiere una clave de API para funcionar. Esta clave te permite acceder al modelo de IA de Google.

  * Ve a [**https://aistudio.google.com/app/apikey**](https://aistudio.google.com/app/apikey)
  * Inicia sesión con tu cuenta de Google.
  * Haz clic en **"Create API key in new project"** y copia la clave generada.

### 3\. Configurar la Clave de API

Para mantener la clave segura, Streamlit usa un archivo de secretos.

  * En la carpeta principal del proyecto, crea una carpeta llamada **`.streamlit`**.
  * Dentro de esa carpeta, crea un archivo llamado **`secrets.toml`**.
  * Abre `secrets.toml` y pega tu clave con el siguiente formato:

<!-- end list -->

```toml
# .streamlit/secrets.toml
API_KEY = "PEGA_AQUÍ_TU_CLAVE_DE_API"
```

## ▶️ Cómo Ejecutar la Aplicación

Una vez que hayas completado la configuración, ejecuta la aplicación desde la terminal en la carpeta del proyecto:

```bash
streamlit run app.py
```

Tu navegador se abrirá automáticamente para mostrarte la aplicación.

-----

## 📄 Archivos del Proyecto

  * **`app.py`**: El código principal de la aplicación Streamlit.
  * **`style.css`**: Hoja de estilos para personalizar el diseño.
  * **`logo.png`**: El logo utilizado en la barra lateral.
  * **`README.md`**: Este archivo.
  * **`.streamlit/secrets.toml`**: Archivo de configuración para la clave de API.
  * **`requirements.txt`**: Listado de dependencias para Python.

## 📜 Contenido de `requirements.txt`

Crea un archivo de texto en la carpeta principal del proyecto llamado `requirements.txt` y pega el siguiente contenido:

```
streamlit
requests
```

-----

## 👨‍💻 Autor

Creado por Sergio Felipe Garcia.

