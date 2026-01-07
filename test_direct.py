import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import pandas as pd
import numpy as np
# ... (gardez vos autres imports : uuid, json, zipfile, etc.)

# --- CHARGEMENT DES DONNÉES (MODE ROBUSTE) ---

def load_data_from_gsheets():
    try:
        # 1. On récupère l'URL depuis les secrets
        base_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        
        # 2. On extrait l'ID de la feuille (entre /d/ et /edit)
        sheet_id = base_url.split("/d/")[1].split("/edit")[0]
        
        # 3. On construit les URLs de téléchargement direct (comme dans le Test A)
        url_q = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Questions"
        url_s = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sites"
        
        # 4. Lecture avec Pandas
        df_questions = pd.read_csv(url_q)
        df_sites = pd.read_csv(url_s)
        
        return df_questions, df_sites
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        return None, None
