import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Evaluación Hackathon", page_icon="🏆", layout="centered")

# ==============================================================================
# CONFIGURACIÓN PRIVADA DE WEBHOOK
# ==============================================================================
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyM8feFteFynfKVBk_L_ypJ6NP08ufGHODv6iGu8v7E8jkUoSRuic54mgPmYfvn2m5gEg/exec"
# ==============================================================================

st.title("🏆 Rúbrica de Evaluación Hackathon")

st.divider()

# Datos Generales
st.subheader("📋 Datos Generales")
col1, col2 = st.columns(2)
with col1:
    evaluador = st.text_input("Evaluador*", placeholder="Ej. Gustavo")
with col2:
    equipo = st.text_input("Equipo*", placeholder="Ej. Nicolas")

st.divider()

# Criterios de Evaluación
st.subheader("📊 Criterios de Evaluación")

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

if st.button("🚀 Guardar Evaluación", type="primary", use_container_width=True, key="btn_guardar_evaluacion"):
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