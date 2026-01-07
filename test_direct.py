import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diagnostic Connexion Directe", layout="wide")

st.title("🧪 Test de Diagnostic : Connexion Directe")

# 1. Vérification de la présence des Secrets
if "connections" not in st.secrets or "gsheets" not in st.secrets["connections"]:
    st.error("❌ Le secret '[connections.gsheets]' est manquant dans vos paramètres Streamlit.")
    st.stop()

base_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
st.info(f"🔗 URL détectée dans les secrets : `{base_url}`")

# 2. Extraction de l'ID de la feuille
try:
    if "/d/" in base_url:
        sheet_id = base_url.split("/d/")[1].split("/")[0]
        st.success(f"🆔 ID de la feuille extrait : `{sheet_id}`")
    else:
        st.error("❌ L'URL dans les secrets ne semble pas être une URL Google Sheets valide.")
        st.stop()
except Exception as e:
    st.error(f"❌ Erreur lors de l'extraction de l'ID : {e}")
    st.stop()

# 3. Tentative de lecture des onglets
def try_load(sheet_name):
    # Construction de l'URL d'export CSV (méthode robuste)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        st.write(f"### ✅ Onglet '{sheet_name}' trouvé")
        st.dataframe(df.head(10)) # Affiche les 10 premières lignes
        return True
    except Exception as e:
        st.error(f"❌ Impossible de lire l'onglet '{sheet_name}'")
        st.warning(f"Détail de l'erreur : {e}")
        return False

col1, col2 = st.columns(2)

with col1:
    success_q = try_load("Questions")

with col2:
    success_s = try_load("Sites")

# 4. Conclusion du diagnostic
st.markdown("---")
if success_q and success_s:
    st.balloons()
    st.success("✨ Félicitations ! La méthode directe fonctionne parfaitement avec vos fichiers.")
    st.info("💡 Vous pouvez maintenant utiliser cette logique dans votre fichier `utils.py` pour corriger l'application.")
else:
    st.error("🚨 Le diagnostic a échoué pour un ou plusieurs onglets.")
    st.write("Vérifiez que :")
    st.write("1. Les noms des onglets sont exactement 'Questions' et 'Sites' (attention aux majuscules).")
    st.write("2. Le partage est bien sur 'Tous les utilisateurs disposant du lien : Lecteur ou Éditeur'.")
