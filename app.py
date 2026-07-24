import streamlit as st
import requests
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Evaluación Hackathon", page_icon="🏆", layout="centered")

# ==============================================================================
# ESTILOS CSS PERSONALIZADOS (Capas de diseño sin alterar la lógica)
# ==============================================================================
st.markdown("""
<style>
    /* Fondo general suave */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Banner/Encabezado Superior Rediseñado para Logo y Texto */
    .hero-header {
        background: linear-gradient(135deg, #07090C 0%, #151A24 100%); /* Fondo azul navy muy oscuro */
        color: #FFFFFF;
        padding: 1rem 1.8rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center; /* Alineación vertical */
        justify-content: flex-start; /* Logo a la izquierda */
    }
    .header-logo {
        max-height: 80px; /* control de tamaño del logo */
        width: auto;
        margin-right: 2rem; /* separación entre logo y texto */
    }
    .header-text {
        flex-grow: 1; /* ocupa el resto del espacio */
        text-align: center; /* centra el texto en su espacio */
    }
    .hero-header h1 {
        color: #FFFFFF !important;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .hero-header p {
        color: #94A3B8;
        margin-top: 0.4rem;
        font-size: 0.95rem;
        margin-bottom: 0;
    }

    /* Tarjetas de sección (para Datos Generales y Criterios) */
    div[data-testid="stForm"] > div > div {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }

    /* Tarjeta para la métrica del Puntaje Total */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 1.2rem 1.8rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
        text-align: center;
        margin-top: 1rem;
    }

    /* Botón de envío estilizado */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        font-size: 1.05rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #1D4ED8 0%, #1E40AF 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# CONFIGURACIÓN PRIVADA DE WEBHOOK (Mantenida intacta)
# ==============================================================================
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyM8feFteFynfKVBk_L_ypJ6NP08ufGHODv6iGu8v7E8jkUoSRuic54mgPmYfvn2m5gEg/exec"
# ==============================================================================

# Header Principal Estilizado con Logo e Institucional
st.markdown("""
    <div class="hero-header">
        <img src="./logo.png" class="header-logo" alt="Organización Logo">
        <div class="header-text">
            <h1>🏆 Rúbrica de Evaluación Hackathon</h1>
            <p>Portal Oficial del Jurado</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Lógica del Formulario con el diseño moderno
with st.form("form_evaluacion"):
    # Sección 1: Datos Generales
    st.markdown("<h3>📋 Datos Generales</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        evaluador = st.text_input("Evaluador*", placeholder="Ej. Gustavo")
    with col2:
        equipo = st.text_input("Equipo*", placeholder="Ej. Nicolas")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Sección 2: Criterios de Evaluación (Mantenidos exactamente)
    st.markdown("<h3>📊 Criterios de Evaluación</h3>", unsafe_allow_html=True)

    c1 = st.slider("1. Escenario", 0, 15, 10)
    c2 = st.slider("2. Infraestructura y Energía", 0, 15, 10)
    c3 = st.slider("3. Comunicación e Información", 0, 15, 10)
    c4 = st.slider("4. Coordinación y Logística", 0, 15, 10)
    c5 = st.slider("5. Atención a la Población", 0, 15, 10)
    c6 = st.slider("6. Operación de Emergencia", 0, 15, 10)
    c7 = st.slider("7. Enfoque Interdisciplinario", 0, 10, 5)

    total_score = c1 + c2 + c3 + c4 + c5 + c6 + c7

    st.metric(label="🎯 Puntaje Total", value=f"{total_score} pts")

    observaciones = st.text_area("💬 Observaciones", placeholder="Comentarios...")

    # Botón de envío (Mantenido funcionalmente)
    submitted = st.form_submit_button("🚀 Guardar Evaluación", type="primary", use_container_width=True)

# Lógica de envío al Webhook (Mantenida intacta)
if submitted:
    if not evaluador.strip() or not equipo.strip():
        st.warning("⚠️ Por favor completa el Evaluador y el Equipo.")
    elif not WEBHOOK_URL.startswith("http"):
        st.error("⚠️ La URL del Webhook no es válida.")
    else:
        payload = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "evaluador": evaluador,
            "equipo": equipo,
            "escenario": c1,
            "infraestructura_energia": c2,
            "comunicacion_info": c3,
            "coordinacion_logistica": c4,
            "atencion_poblacion": c5,
            "operacion_emergencia": c6,
            "enfoque_interdisciplinario": c7,
            "puntaje_total": total_score,
            "observaciones": observaciones
        }

        with st.spinner("Guardando en Google Sheets..."):
            try:
                response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
                if response.status_code in [200, 201]:
                    st.success("✅ ¡Evaluación y puntajes guardados correctamente!")
                    st.balloons()
                else:
                    st.error(f"❌ Error al enviar. Código: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error de conexión: {e}")
