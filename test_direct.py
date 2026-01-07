import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🧪 Test de Connexion via Secrets")

try:
    # Tentative de connexion via le connecteur Streamlit
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Tentative de lecture de l'onglet 'Questions'
    df = conn.read(worksheet="Questions")
    
    st.success("✅ Les Secrets sont bien configurés et fonctionnels !")
    st.dataframe(df.head())
    
except Exception as e:
    st.error("❌ Erreur de configuration des Secrets.")
    st.exception(e)
    st.info("Vérifiez que votre section [connections.gsheets] est bien présente dans les Secrets.")
