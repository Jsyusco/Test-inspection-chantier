import streamlit as st
import pandas as pd
import uuid
import urllib.parse
from datetime import datetime
import utils
import streamlit.components.v1 as components

# --- FONCTION PWA ---
def inject_pwa_full():
    icon_url = "https://raw.githubusercontent.com/Jsyusco/Audit-installateurs/main/logo.png?v=2"
    manifest_url = "https://raw.githubusercontent.com/Jsyusco/Audit-installateurs/main/manifest.json"
    pwa_html = f"""
    <script>
        const head = window.parent.document.head;
        if (!head.querySelector('link[rel="apple-touch-icon"]')) {{
            const appleIcon = window.parent.document.createElement('link');
            appleIcon.rel = 'apple-touch-icon';
            appleIcon.href = '{icon_url}';
            head.appendChild(appleIcon);
        }}
        if (!head.querySelector('link[rel="manifest"]')) {{
            const manifest = window.parent.document.createElement('link');
            manifest.rel = 'manifest';
            manifest.href = '{manifest_url}';
            head.appendChild(manifest);
        }}
    </script>"""
    components.html(pwa_html, height=0)

# --- CONFIGURATION PAGE ---
st.set_page_config(
    page_title="Audit Installateurs",
    page_icon="https://raw.githubusercontent.com/Jsyusco/Audit-installateurs/main/logo.png",
    layout="centered"
)

inject_pwa_full()

# --- STYLE CSS (Adapté Dark/Light) ---
st.markdown("""
<style>
    .main-header { background-color: var(--secondary-background-color); padding: 20px; border-radius: 10px; text-align: center; border-bottom: 3px solid #E9630C; margin-bottom: 20px; color: var(--text-color); }
    .question-card { border-left: 5px solid #E9630C; padding: 15px; margin-bottom: 20px; background-color: rgba(128,128,128,0.1); border-radius: 5px; }
    .error-box { background-color: rgba(255,0,0,0.1); border: 1px solid #ff4b4b; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- AUTHENTIFICATION SÉCURISÉE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="main-header"><h1>🔐 Accès Restreint</h1></div>', unsafe_allow_html=True)
    with st.container(border=True):
        pwd = st.text_input("Code d'accès installateur", type="password")
        if st.button("Se connecter"):
            if pwd == st.secrets["ACCESS_CODE"]:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Code incorrect")
    st.stop()

# --- INITIALISATION ÉTAT ---
def init_session_state():
    if 'step' not in st.session_state:
        st.session_state.update({
            'step': 'PROJECT_LOAD',
            'project_data': None,
            'collected_data': [],
            'current_phase_index': 0,
            'current_phase_temp_answers': {},
            'submission_id': str(uuid.uuid4()),
            'form_start_time': datetime.now(),
            'data_saved': False,
            'df_struct': None,
            'df_site': None
        })

init_session_state()

# --- LOGIQUE DE L'APP ---
if st.session_state['step'] == 'PROJECT_LOAD':
    with st.spinner("Chargement des données..."):
        st.session_state['df_struct'] = utils.load_form_structure_from_firestore()
        st.session_state['df_site'] = utils.load_site_data_from_firestore()
        if st.session_state['df_struct'] is not None:
            st.session_state['step'] = 'PROJECT'
            st.rerun()

elif st.session_state['step'] == 'PROJECT':
    st.markdown('<div class="main-header"><h1>🏗️ Sélection du Projet</h1></div>', unsafe_allow_html=True)
    search = st.text_input("Rechercher un projet (Ville)")
    if len(search) >= 3:
        df_site = st.session_state['df_site']
        filtered = df_site[df_site['Intitulé'].str.contains(search, case=False, na=False)]
        if not filtered.empty:
            choice = st.selectbox("Sélectionnez le chantier", [""] + filtered['Intitulé'].tolist())
            if choice and st.button("Valider"):
                st.session_state['project_data'] = filtered[filtered['Intitulé'] == choice].iloc[0].to_dict()
                st.session_state['step'] = 'FILL_PHASE'
                st.rerun()

elif st.session_state['step'] == 'FILL_PHASE':
    df_q = st.session_state['df_struct']
    phases = df_q['section'].unique().tolist()
    curr_idx = st.session_state['current_phase_index']
    curr_phase = phases[curr_idx]

    st.markdown(f'<div class="main-header"><h1>{curr_phase}</h1></div>', unsafe_allow_html=True)
    
    # Rendu des questions de la phase
    phase_rows = df_q[df_q['section'] == curr_phase]
    for _, row in phase_rows.iterrows():
        utils.render_question(row, st.session_state['current_phase_temp_answers'], curr_phase, "key", 0, st.session_state['project_data'])

    if st.button("Suivant ➡️"):
        # Validation
        valid, errors = utils.validate_section(df_q, curr_phase, st.session_state['current_phase_temp_answers'], st.session_state['collected_data'], st.session_state['project_data'])
        if valid:
            st.session_state['collected_data'].append({"phase_name": curr_phase, "answers": st.session_state['current_phase_temp_answers'].copy()})
            if curr_idx < len(phases) - 1:
                st.session_state['current_phase_index'] += 1
                st.session_state['current_phase_temp_answers'] = {}
                st.rerun()
            else:
                st.session_state['step'] = 'FINISHED'
                st.rerun()
        else:
            for e in errors: st.error(e)

elif st.session_state['step'] == 'FINISHED':
    st.markdown('<div class="main-header"><h1>✅ Audit Terminé</h1></div>', unsafe_allow_html=True)
    project_name = st.session_state['project_data'].get('Intitulé', 'Inconnu')

    if not st.session_state['data_saved']:
        with st.spinner("Enregistrement final..."):
            success, msg = utils.save_form_data(
                st.session_state['collected_data'], 
                st.session_state['project_data'], 
                st.session_state['submission_id'], 
                st.session_state['form_start_time']
            )
            if success: st.session_state['data_saved'] = True

    # Exports
    col1, col2, col3 = st.columns(3)
    # Note: Assurez-vous que vos fonctions utils correspondent à ces appels
    csv_data = utils.create_csv_export(st.session_state['collected_data'], st.session_state['df_struct'], project_name, st.session_state['submission_id'], st.session_state['form_start_time'])
    col1.download_button("📊 CSV", csv_data, f"{project_name}.csv")
    
    zip_buf = utils.create_zip_export(st.session_state['collected_data'])
    if zip_buf: col2.download_button("🖼️ Photos", zip_buf.getvalue(), f"Photos_{project_name}.zip")
    
    word_buf = utils.create_word_report(st.session_state['collected_data'], st.session_state['df_struct'], st.session_state['project_data'], st.session_state['form_start_time'])
    col3.download_button("📄 Word", word_buf.getvalue(), f"Rapport_{project_name}.docx")

    if st.button("🔄 Nouvel Audit"):
        st.session_state.clear()
        st.rerun()
