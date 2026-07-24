import streamlit as st
import requests
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="Evaluación Hackathon", page_icon="🏆", layout="centered")

# ==============================================================================
# ESTILOS CSS - PALETA DE COLOR Y COMPOSICIÓN INSTITUCIONAL
# ==============================================================================
st.markdown("""
<style>
    /* 1. Fondo de la Aplicación (Gris Hielo Pizarra) */
    .stApp {
        background-color: #F1F5F9;
        font-family: 'Inter', sans-serif;
    }
    
    /* 2. Banner/Encabezado Superior (Azul Noche / Pizarra) */
    .hero-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF;
        padding: 1.5rem 2rem;
        border-radius: 14px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.2);
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }
    .header-logo {
        max-height: 110px;
        width: auto;
        margin-right: 2rem;
        filter: drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.3));
    }
    .header-text {
        flex-grow: 1;
        text-align: center;
    }
    .hero-header h1 {
        color: #FFFFFF !important;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .hero-header p {
        color: #94A3B8;
        margin-top: 0.4rem;
        font-size: 0.95rem;
        margin-bottom: 0;
    }

    /* 3. Títulos de Secciones */
    h3 {
        color: #0F172A !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }

    /* 4. Estilo de Inputs y Cajas de Texto */
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        color: #0F172A !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }

    /* 5. Tarjeta del Puntaje Total */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        padding: 1.2rem 1.8rem;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin: 1.5rem 0;
    }
    div[data-testid="stMetric"] label {
        color: #475569 !important;
        font-weight: 600;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #1E3A8A !important;
        font-weight: 800;
    }

    /* 6. Botón de Envío */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 0.85rem 1rem;
        font-weight: 600;
        font-size: 1.05rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #1D4ED8 0%, #1E40AF 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
        transform: translateY(-1px);
    }

    /* Líneas divisorias más suaves */
    hr {
        border-color: #CBD5E1 !important;
        margin: 1.8rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# CONFIGURACIÓN PRIVADA DE WEBHOOK
# ==============================================================================
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyM8feFteFynfKVBk_L_ypJ6NP08ufGHODv6iGu8v7E8jkUoSRuic54mgPmYfvn2m5gEg/exec"
# ==============================================================================

# Encabezado Principal (Usa ?v=2 para refrescar la caché de la imagen)
st.markdown("""
    <div class="hero-header">
        <img src="https://raw.githubusercontent.com/alchemistnick/Hackathon2026/master/logo.png?v=2" class="header-logo" alt="Organización Logo">
        <div class="header-text">
            <h1>🏆 Rúbrica de Evaluación Hackathon</h1>
            <p>Portal Oficial del Jurado</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sección 1: Datos Generales
st.markdown("<h3>📋 Datos Generales</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    evaluador = st.text_input("Evaluador*", placeholder="Ej. Gustavo")
with col2:
    equipo = st.text_input("Equipo*", placeholder="Ej. Nicolas")

st.divider()

# Sección 2: Criterios de Evaluación
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

st.divider()

# Botón de envío
submitted = st.button("🚀 Guardar Evaluación", type="primary", use_container_width=True)

# Lógica de envío al Webhook
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
