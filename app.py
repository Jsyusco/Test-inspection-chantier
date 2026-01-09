import streamlit as st
import streamlit_firebase_auth as auth

st.title("🔍 Test Import Firebase Auth")

try:
    # On vérifie ce que contient réellement le package
    st.write("Contenu du module :", dir(auth))
    
    # Tentative avec le nom de fonction alternatif souvent utilisé dans ce package
    if hasattr(auth, 'firebase_auth'):
        st.success("✅ La fonction 'firebase_auth' existe !")
    elif hasattr(auth, 'streamlit_firebase_auth'):
        st.info("ℹ️ La fonction s'appelle en fait 'streamlit_firebase_auth'")
    else:
        st.warning("⚠️ Aucune des fonctions connues n'est présente.")

except Exception as e:
    st.error(f"Erreur : {e}")
