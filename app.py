import streamlit as st
import sys

st.set_page_config(page_title="Test Installation")

st.title("🔍 Diagnostic d'installation")

st.write("Version Python :", sys.version)

# Test de l'importation
try:
    import streamlit_firebase_auth
    from streamlit_firebase_auth import firebase_auth
    
    st.success("✅ SUCCÈS : La bibliothèque `streamlit-firebase-auth` est bien installée et importée !")
    st.balloons()
    
    st.info("""
    **Prochaine étape :**
    Puisque cela fonctionne ici, vous pouvez remettre votre code complet. 
    Assurez-vous juste de garder la ligne 'streamlit-firebase-auth' dans votre requirements.txt.
    """)

except ImportError as e:
    st.error("❌ ÉCHEC : La bibliothèque est introuvable.")
    st.code(f"Erreur détaillée : {e}")
    
    st.warning("""
    **Causes possibles :**
    1. Le fichier s'appelle 'Requirements.txt' (avec majuscule) ou 'requirements.txt.txt'.
    2. Le fichier n'est pas à la racine du dépôt GitHub (pas dans un dossier).
    3. Streamlit Cloud n'a pas redémarré (Tentez 'Reboot App').
    """)
