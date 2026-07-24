import streamlit as st
import requests

# 1. Configuración de la página
st.set_page_config(
    page_title="Evaluación | Hackathon 2026",
    page_icon="🏆",
    layout="centered"
)

# 2. Inyección de CSS personalizado para estilizar la UI
st.markdown("""
<style>
    /* Estilo general y tipografía */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Encabezado principal */
    .hero-header {
        background: linear-gradient(135deg, #1E293B 0%, #312E81 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    .hero-header h1 {
        color: #FFFFFF !important;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .hero-header p {
        color: #C7D2FE;
        font-size: 1.1rem;
    }

    /* Botón de envío */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #4F46E5 0%, #4338CA 100%);
        color: white !important;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
    }

    /* Tarjetas de sección */
    div[data-testid="stForm"] {
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        background-color: #FFFFFF;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Webhook URL (obtenido de Google Apps Script)
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyM8feFteFynfKVBk_L_ypJ6NP08ufGHODv6iGu8v7E8jkUoSRuic54mgPmYfvn2m5gEg/exec"

# Banner Superior
st.markdown("""
    <div class="hero-header">
        <h1>🏆 Portal de Evaluación</h1>
        <p>Hackathon 2026 — Panel del Jurado</p>
    </div>
""", unsafe_allow_html=True)

# Formulario de Evaluación
with st.form("form_evaluacion", clear_on_submit=True):
    
    st.subheader("📌 Datos Principales")
    col1, col2 = st.columns(2)
    with col1:
        jurado = st.text_input("Nombre del Jurado", placeholder="Ej. Ana Martínez")
    with col2:
        equipo = st.selectbox(
            "Equipo / Proyecto", 
            ["Seleccionar...", "Equipo 1 - TechAI", "Equipo 2 - GreenData", "Equipo 3 - HealthApp", "Equipo 4 - FinTech"]
        )
    
    st.divider()
    st.subheader("📊 Criterios de Evaluación (1 al 10)")
    
    c1, c2 = st.columns(2)
    with c1:
        innovacion = st.slider("💡 Innovación y Creatividad", 1, 10, 5, key="s_inn")
        viabilidad = st.slider("⚙️ Viabilidad Técnica", 1, 10, 5, key="s_via")
    with c2:
        diseno = st.slider("🎨 UX / UI y Diseño", 1, 10, 5, key="s_dis")
        pitch = st.slider("🎤 Presentación / Pitch", 1, 10, 5, key="s_pit")

    st.divider()
    
    # Muestra visual del puntaje total calculado
    puntaje_total = innovacion + viabilidad + diseno + pitch
    st.metric(label="Puntaje Total Calculado", value=f"{puntaje_total} / 40 pts")

    comentarios = st.text_area("💬 Comentarios o Feedback para el equipo", placeholder="Escribe aquí feedback constructivo...")
    
    submitted = st.form_submit_button("🚀 Registrar Evaluación")

# Lógica de envío al Webhook
if submitted:
    if not jurado or equipo == "Seleccionar...":
        st.warning("⚠️ Por favor completa tu nombre y selecciona un equipo antes de enviar.")
    else:
        payload = {
            "jurado": jurado,
            "equipo": equipo,
            "innovacion": innovacion,
            "viabilidad": viabilidad,
            "diseno": diseno,
            "pitch": pitch,
            "total": puntaje_total,
            "comentarios": comentarios
        }
        
        try:
            res = requests.post(WEBHOOK_URL, json=payload)
            if res.status_code == 200:
                st.success(f"✅ ¡Evaluación para '{equipo}' registrada con éxito!")
            else:
                st.error("Error al registrar en la base de datos.")
        except Exception as e:
            st.error(f"Error de conexión: {e}")
