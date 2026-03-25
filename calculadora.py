import streamlit as st
import math
import json
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# --- CONFIGURACIÓN HABITA J&B ---
st.set_page_config(page_title="HabitA J&B - Gestión de Obra", page_icon="🏗️", layout="wide")

# --- FUNCIONES DE GUARDADO ---
def guardar_proyecto(nombre, datos):
    proyectos = cargar_proyectos()
    proyectos[nombre] = datos
    with open('proyectos_habita.json', 'w') as f:
        json.dump(proyectos, f)

def cargar_proyectos():
    if os.path.exists('proyectos_habita.json'):
        with open('proyectos_habita.json', 'r') as f:
            return json.load(f)
    return {}

# --- INTERFAZ ---
st.title("🏗️ Sistema HabitA J&B (Móvil)")
st.sidebar.header("Menú de Obra")

servicio = st.sidebar.selectbox(
    "Selecciona el servicio:",
    ["Tablaroca (Muros/Cajillos)", "Piso / Loseta", "Pintura", "Planos e Instalaciones", "Guía Técnica", "Historial de Proyectos"]
)

with st.sidebar:
    st.write("---")
    desperdicio = st.slider("Margen de error (%)", 5, 25, 10)
    factor = 1 + (desperdicio / 100)

# --- 1. TABLAROCA ---
if servicio == "Tablaroca (Muros/Cajillos)":
    st.header("🛠️ Calculadora de Tablaroca")
    modo = st.radio("Tipo de cálculo:", ["Muro Individual", "Casa Completa (11.60x6.50)"])
    
    col1, col2 = st.columns(2)
    with col1:
        largo = st.number_input("Largo (m)", value=3.0, step=0.10)
        alto = st.number_input("Alto (m)", value=2.4, step=0.10)
    with col2:
        espesor = st.number_input("Espesor (m)", value=0.10, step=0.01)
        separacion = st.selectbox("Postes cada (cm):", [30, 40, 61], index=2)

    if st.button("🧮 CALCULAR MATERIAL"):
        if modo == "Muro Individual":
            area = ((largo * alto) * 2) + (alto * espesor * 2) + (largo * espesor)
            lin = largo
        else:
            lin = (11.60 * 2) + (6.50 * 2)
            area = lin * 2.40
            
        hojas = math.ceil((area / 2.97) * factor)
        postes = math.ceil((lin / (separacion/100)) + 2)
        canales = math.ceil((lin * 2) / 3.05)
        
        st.success(f"**RESULTADOS:**")
        st.write(f"📄 **Hojas:** {hojas} | 🏗️ **Postes:** {postes} | 🔲 **Canales:** {canales}")
        st.write(f"🔩 **Tornillo 1-1/4:** {hojas*35} | 🔩 **Tornillo 7/16:** {(postes*4)+(canales*6)}")

# --- 2. PISO ---
elif servicio == "Piso / Loseta":
    st.header("🧱 Cálculo de Piso")
    l_p = st.number_input("Largo (m)", value=4.0, step=0.1)
    a_p = st.number_input("Ancho (m)", value=4.0, step=0.1)
    
    if st.button("🧮 CALCULAR PISO"):
        area = l_p * a_p
        st.success(f"Área: {area:.2f} m²")
        st.write(f"📦 Cajas: {math.ceil((area/1.5)*factor)} | 🥣 Sacos: {math.ceil(area/4)}")

# --- 3. PINTURA ---
elif servicio == "Pintura":
    st.header("🎨 Cálculo de Pintura")
    area_m2 = st.number_input("m² a pintar", value=20.0)
    
    if st.button("🧮 CALCULAR PINTURA"):
        litros = math.ceil(((area_m2 / 10) * 2) * factor)
        st.success(f"Necesitas: {litros} Litros ({math.ceil(litros/19)} cubetas)")

# --- 4. PLANOS ---
elif servicio == "Planos e Instalaciones":
    st.header("📸 Escáner de Planos")
    archivo = st.file_uploader("Sube o toma foto:", type=["jpg", "png", "jpeg"])
    
    if archivo:
        img = Image.open(archivo)
        col_marcador, col_canvas = st.columns([1, 3])
        with col_marcador:
            color = st.color_picker("Color:", "#FFFB00")
            st.write("🟡 Luz | 🔵 Agua | 🔴 Drenaje")
        
        with col_canvas:
            st_canvas(fill_color="rgba(255,165,0,0.3)", stroke_width=5, stroke_color=color,
                      background_image=img, height=400, drawing_mode="freedraw", key="cel_canvas")

# --- 5. GUÍA TÉCNICA ---
elif servicio == "Guía Técnica":
    st.header("📚 Manual HabitA J&B")
    st.markdown("""
    - **Luz:** Contactos (Cal 12), Focos (Cal 14).
    - **Drenaje:** WC (4"), Lavabos (2"). **Pendiente:** 2cm/metro.
    - **Agua:** Salidas (1/2"), Principal (3/4").
    """)

# --- 6. HISTORIAL ---
elif servicio == "Historial de Proyectos":
    st.header("📂 Obras Guardadas")
    proyectos = cargar_proyectos()
    for p in proyectos:
        st.info(f"📋 {p}")

st.sidebar.write("---")
st.sidebar.write("© 2026 **HabitA J&B** | Tijuana")