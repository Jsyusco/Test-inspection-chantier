import streamlit as st
import pandas as pd

st.title("🧪 Test de Connexion Directe")

# L'ID de votre feuille (extrait de votre URL)
SHEET_ID = "1U7atj3w4ajsJydEBXKY8HbIKuijKu6CA3sS6FYKYsAw"
SHEET_NAME = "Questions" # Testons d'abord cet onglet

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

try:
    df = pd.read_csv(url)
    st.success("✅ Connexion réussie !")
    st.write("Voici les 5 premières lignes de l'onglet 'Questions' :")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"❌ Échec de la connexion directe : {e}")
