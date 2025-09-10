import streamlit as st
import requests
import json
from datetime import datetime
import io
import re

# Configuración de la página
st.set_page_config(
    page_title="Generador de Plantillas WhatsApp",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para diseño comercial
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Función para generar plantillas con IA
def generar_plantillas(datos_formulario):
    api_key = st.secrets["API_KEY"]
    model = 'gemini-2.0-flash-exp'
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
    
    prompt = f"""
    Eres un experto en comunicación empresarial a través de WhatsApp. Desarrolla 2 plantillas de mensajes optimizadas para maximizar
    la interacción y conversión, cumpliendo estrictamente con las políticas de WhatsApp. Estructura el resultado de forma clara.
    
    Datos del cliente:
    - Nombre de la Marca o Negocio: {datos_formulario['negocio']}
    - Sector: {datos_formulario['sector']}
    - Objetivo: {datos_formulario['objetivo']}
    - Audiencia: {datos_formulario['audiencia']}
    - Detalles: {datos_formulario['detalles']}
    - Idioma: {datos_formulario['idioma']}
    - Botones interactivos: {datos_formulario['botones']}
    
    Instrucciones:
    Crea 2 plantillas con esta estructura:
    Nombre de la plantilla: [Nombre único]
    Categoría: [marketing/utilidad/autenticación]
    Idioma: [Idioma]
    Componentes:
        Cabecera: [Tipo y contenido]
        Cuerpo: [Mensaje principal]
        Botones: [Hasta 3 botones]
        Propósito: [Descripción breve]
    
    Sugerencias de Respuesta:
    - Ejemplo de respuesta breve
    - Flujo de seguimiento
    - Elementos adicionales
    
    Cumplimiento de Políticas:
    - Relevancia para el cliente
    - Sin contenido promocional excesivo
    - Tono conversacional
    - Propósito claro
    
    Formato de Respuesta:
    PLANTILLA 1
    [Contenido detallado]
    --------------------------------------------------
    PLANTILLA 2
    [Contenido detallado]
    """
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        st.error(f"Error al generar plantillas: {str(e)}")
        return None

# Función para formatear texto para visualización
def formatear_plantilla(texto):
    patrones = [
        (r'Nombre de la plantilla:', '### **Nombre de la plantilla:**'),
        (r'Categoría:', '### **Categoría:**'),
        (r'Idioma:', '### **Idioma:**'),
        (r'Componentes:', '### **Componentes:**'),
        (r'Cabecera:', '#### **Cabecera:**'),
        (r'Cuerpo:', '#### **Cuerpo:**'),
        (r'Botones:', '#### **Botones:**'),
        (r'Propósito:', '### **Propósito:**'),
        (r'Sugerencias de Respuesta:', '### **Sugerencias de Respuesta:**'),
        (r'Flujo de seguimiento:', '#### **Flujo de seguimiento:**'),
        (r'Elementos adicionales:', '#### **Elementos adicionales:**'),
        (r'Cumplimiento de Políticas:', '### **Cumplimiento de Políticas:**'),
        (r'Relevancia para el cliente:', '- **Relevancia para el cliente:**'),
        (r'Sin contenido promocional excesivo:', '- **Sin contenido promocional excesivo:**'),
        (r'Tono conversacional:', '- **Tono conversacional:**'),
        (r'Propósito claro:', '- **Propósito claro:**'),
    ]
    
    texto_formateado = texto
    for patron, reemplazo in patrones:
        texto_formateado = re.sub(patron, reemplazo, texto_formateado)
    
    texto_formateado = texto_formateado.replace('\n', '\n\n')
    texto_formateado = re.sub(r'\n\s*\n', '\n\n', texto_formateado)
    
    return texto_formateado

# Extraer componentes clave de la plantilla
def parsear_componentes(texto):
    cabecera = ""
    cuerpo = ""
    botones = []

    cabecera_match = re.search(r'Cabecera:\s*(.*)', texto, re.I)
    if cabecera_match:
        cabecera = cabecera_match.group(1).strip()

    cuerpo_match = re.search(r'Cuerpo:\s*(.*)', texto, re.I)
    if cuerpo_match:
        cuerpo = cuerpo_match.group(1).strip()

    botones_match = re.search(r'Botones:\s*(.*?)(?:Propósito:|$)', texto, re.S | re.I)
    if botones_match:
        botones_str = botones_match.group(1).strip()
        botones = re.split(r'[\n,;-]+', botones_str)
        botones = [b.strip().strip('"') for b in botones if b.strip()]

    return cabecera, cuerpo, botones

# Función para generar archivo TXT
def generar_txt(plantillas, datos_formulario):
    contenido = f"""PLANTILLAS DE WHATSAPP PERSONALIZADAS
========================================

Negocio: {datos_formulario['negocio']}
Sector: {datos_formulario['sector']}
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}

========================================

{plantillas}

========================================
Generado por WhatsApp Template Pro
https://tu-web.com
"""
    txt_buffer = io.StringIO()
    txt_buffer.write(contenido)
    txt_buffer.seek(0)
    txt_bytes = txt_buffer.getvalue().encode('utf-8')
    txt_buffer = io.BytesIO(txt_bytes)
    return txt_buffer

# Función para mostrar plantillas con emojis
def mostrar_plantilla(texto):
    texto_html = texto.replace('\n', '<br>')
    return f"""
    <div class="plantilla-card emoji-container">
        {texto_html}
    </div>
    """

# Mockup de WhatsApp mostrando solo Cabecera, Cuerpo y Botones
def mostrar_en_mockup_componentes(cabecera, cuerpo, botones, negocio):
    botones_html = ""
    if botones:
        botones_html = '<div class="whatsapp-buttons">' + "".join(
            f'<div class="whatsapp-button">{b}</div>' for b in botones[:3]
        ) + '</div>'

    cabecera_html = f"<div class='chat-bubble'><b>{cabecera}</b></div>" if cabecera else ""

    return f"""
    <div class="whatsapp-frame">
        <div class="whatsapp-header">{negocio}</div>
        <div class="whatsapp-chat">
            {cabecera_html}
            <div class="chat-bubble">{cuerpo}</div>
            {botones_html}
        </div>
    </div>
    """

# Interfaz principal
def main():
    with st.sidebar:
        st.image("FotoPerfilSergio.png", width=120)
        st.title("WhatsApp Template Pro")
        st.markdown("""
        **La solución profesional para crear plantillas de WhatsApp efectivas**
        
        Beneficios:
        - Plantillas optimizadas para conversiones
        - Cumplimiento con políticas de WhatsApp
        - Generación en segundos
        - Soporte multiidioma
        """)
        st.markdown("---")
        st.markdown("© 2025 WhatsApp Template Pro. Todos los derechos reservados.")
    
    st.title("Generador de Plantillas de WhatsApp")
    st.markdown("### Crea plantillas profesionales para tu negocio en segundos")
    st.markdown("---")
    st.markdown("## ✨ ¿Para qué sirve esta herramienta?")
    st.markdown("""
    Nuestra aplicación te ayuda a diseñar plantillas de WhatsApp Business que cumplen con los requisitos de Meta y transmiten una imagen profesional, clara y cercana a tus clientes.
    
    ✅ **Ahorra tiempo**: genera plantillas listas para aprobación en cuestión de minutos.
    
    ✅ **Gana confianza**: mensajes bien estructurados que refuerzan la imagen de tu marca.
    
    ✅ **Mejora resultados**: plantillas optimizadas para aumentar la tasa de apertura y respuesta.
    
    ✅ **Evita rechazos y bloqueos**: cumple con las políticas de WhatsApp y protege la reputación de tu número.
    
    Con esta herramienta podrás transformar tus mensajes en comunicaciones estratégicas, listas para ventas, soporte o marketing, asegurando que cada contacto con tus clientes sea efectivo y memorable.
    """)
    st.markdown("---")
    
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'plantillas' not in st.session_state:
        st.session_state.plantillas = None
    if 'datos_formulario' not in st.session_state:
        st.session_state.datos_formulario = None
    
    with st.form("form_plantillas"):
        st.markdown("### Completa los datos de tu negocio")
        col1, col2 = st.columns(2)
        
        with col1:
            negocio = st.text_input("Nombre de tu negocio o marca*", help="Nombre comercial de tu empresa")
            sector = st.selectbox("Sector*", [
                "Retail", "Servicios", "Salud", "Educación", 
                "Finanzas", "Tecnología", "Hostelería", "Otro"
            ])
            objetivo = st.selectbox("Objetivo principal*", [
                "Promoción de productos", "Recordatorio de citas", 
                "Confirmación de pedidos", "Encuestas", 
                "Soporte al cliente", "Otro"
            ])
        
        with col2:
            audiencia = st.text_area("Describe tu audiencia*", help="Ej: Jóvenes entre 18-25 años, madres, profesionales, etc.")
            idioma = st.selectbox("Idioma*", ["Español", "Inglés", "Francés", "Portugués", "Alemán", "Italiano"])
            botones = st.selectbox("¿Incluir botones interactivos?", ["Sí", "No"])
            detalles = st.text_area("Detalles adicionales", help="Cualquier información específica que deba incluirse")
        
        submitted = st.form_submit_button("Generar Plantillas", use_container_width=True)
        
        if submitted:
            if not negocio or not audiencia:
                st.error("Por favor completa los campos obligatorios (*)")
                st.session_state.submitted = False
            else:
                st.session_state.submitted = True
                st.session_state.datos_formulario = {
                    'negocio': negocio,
                    'sector': sector,
                    'objetivo': objetivo,
                    'audiencia': audiencia,
                    'idioma': idioma,
                    'botones': botones,
                    'detalles': detalles
                }
    
    if st.session_state.submitted and st.session_state.datos_formulario:
        with st.spinner("Generando plantillas profesionales..."):
            plantillas = generar_plantillas(st.session_state.datos_formulario)
            st.session_state.plantillas = plantillas
        
        if st.session_state.plantillas:
            st.success("¡Plantillas generadas con éxito!")
            st.markdown("## Tus Plantillas Personalizadas")
            partes = st.session_state.plantillas.split('--------------------------------------------------')
            
            col1, col2 = st.columns(2)
            with col1:
                if len(partes) > 0:
                    st.markdown("### Plantilla 1")
                    plantilla1_formateada = formatear_plantilla(partes[0].replace('PLANTILLA 1', ''))
                    cabecera1, cuerpo1, botones1 = parsear_componentes(partes[0])
                    st.markdown(mostrar_plantilla(plantilla1_formateada), unsafe_allow_html=True)
                    st.markdown("#### Vista previa en WhatsApp 📱")
                    st.markdown(mostrar_en_mockup_componentes(cabecera1, cuerpo1, botones1 if st.session_state.datos_formulario['botones']=="Sí" else [], st.session_state.datos_formulario['negocio']), unsafe_allow_html=True)
            
            with col2:
                if len(partes) > 1:
                    st.markdown("### Plantilla 2")
                    plantilla2_formateada = formatear_plantilla(partes[1].replace('PLANTILLA 2', ''))
                    cabecera2, cuerpo2, botones2 = parsear_componentes(partes[1])
                    st.markdown(mostrar_plantilla(plantilla2_formateada), unsafe_allow_html=True)
                    st.markdown("#### Vista previa en WhatsApp 📱")
                    st.markdown(mostrar_en_mockup_componentes(cabecera2, cuerpo2, botones2 if st.session_state.datos_formulario['botones']=="Sí" else [], st.session_state.datos_formulario['negocio']), unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### ¿Qué deseas hacer con tus plantillas?")
            
            col1, col2 = st.columns(2)
            with col1:
                txt_buffer = generar_txt(st.session_state.plantillas, st.session_state.datos_formulario)
                st.download_button(
                    label="📥 Descargar TXT",
                    data=txt_buffer,
                    file_name=f"plantillas_whatsapp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                if st.button("🔄 Generar Nuevas Plantillas", use_container_width=True):
                    st.session_state.submitted = False
                    st.session_state.plantillas = None
                    st.session_state.datos_formulario = None
                    st.rerun()

if __name__ == "__main__":
    main()
