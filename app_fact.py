#Importacion de Librerias
import streamlit as st
import re
import os
import PyPDF2
import pandas as pd
import zipfile
from st_social_media_links import SocialMediaIcons
import glob

# Configuración de la página de Streamlit
st.set_page_config(page_title="Extraer Datos PDF", page_icon=":books:", layout="wide")

# Función para extraer datos de los PDFs
def extract_data_from_pdfs(files):
    num_fact = []
    fecha = []
    cliente = []
    Iva = []
    Total = []
    nombres = []

    for file in files:
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            page = pdf_reader.pages[0]
            text = page.extract_text()
            
            lines = text.split('\n')
            nombres.append(file.name)

            factura = None
            fecha_fact = None
            cliente_fact = None
            iva_fact = None
            total_fact = None

            for i, line in enumerate(lines):
                if "Nº de factura:" in line:
                    factura = (line.split("Nº de factura:")[1]).strip()
                if "Fecha:" in line:
                    fecha_fact = (line.split("Fecha:")[1]).strip()
                if "Facturar a" in line and i + 1 < len(lines):
                    cliente_fact = lines[i + 1].strip()
                if "Iva" in line:
                    iva_fact = re.search(r'\$?([\d.,]+)', line)
                    if iva_fact:
                        iva_fact = iva_fact.group(1).replace(',', '').strip()
                if "Total" in line:
                    total_fact = re.search(r'\$?([\d.,]+)', line)
                    if total_fact:
                        total_fact = total_fact.group(1).replace(',', '').strip()

            iva_fact = iva_fact if iva_fact else "No encontrado"
            total_fact = total_fact if total_fact else "No encontrado"

            num_fact.append(factura if factura else "No encontrado")
            fecha.append(fecha_fact if fecha_fact else "No encontrado")
            cliente.append(cliente_fact if cliente_fact else "No encontrado")
            Iva.append(iva_fact)
            Total.append(total_fact)

        except Exception as e:
            st.error(f"Error al procesar {file.name}: {e}")

    data = {'Archivo': nombres, 'Factura': num_fact, 'Fecha': fecha, 'Cliente': cliente, 'Iva': Iva, 'Total': Total}
    df = pd.DataFrame(data)
    return df

# Interfaz de Streamlit
st.title("Extracción de Datos PDF")
st.write("Sube tus archivos PDF para extraer los datos.")

# Subir archivos PDF
uploaded_files = st.file_uploader("Sube tus archivos PDF", type="pdf", accept_multiple_files=True)

if uploaded_files:
    df = extract_data_from_pdfs(uploaded_files)
    st.write(df)

# Pie de página con información del desarrollador y logos de redes sociales
st.markdown("""
---
**Desarrollador:** Edwin Quintero Alzate<br>
**Email:** egqa1975@gmail.com<br>
""")

social_media_links = [
    "https://www.facebook.com/edwin.quinteroalzate",
    "https://www.linkedin.com/in/edwinquintero0329/",
    "https://github.com/Edwin1719"]

social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()