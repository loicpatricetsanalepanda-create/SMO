import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Charger les variables secrètes (.env)
load_dotenv()

# ==========================================
# 1. DESIGN SYSTEM PROPRIÉTAIRE (STYLE GEMINI)
# ==========================================
st.set_page_config(
    page_title="SMO IA",
    page_icon="☘️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Injection CSS pour appliquer le design épuré sans bordure de Gemini
st.markdown("""
    <style>
    /* Fond noir mat uniforme */
    .stApp {
        background-color: #0e0e10 !important;
        color: #e3e3e3 !important;
    }
    
    /* Nettoyage de l'interface Streamlit */
    header, footer, [data-testid="stDecoration"] {
        visibility: hidden !important;
        height: 0px !important;
    }
    
    /* Barre latérale sombre */
    [data-testid="stSidebar"] {
        background-color: #171719 !important;
        border-right: 1px solid #222327 !important;
    }
    
    /* Titre d'accueil centré */
    .gemini-title {
        font-family: 'Google Sans', 'Inter', sans-serif;
        font-weight: 400;
        font-size: 2.5rem;
        color: #ffffff;
        text-align: center;
        margin-top: 6rem;
        margin-bottom: 2.5rem;
    }
    
    /* Boutons Suggestions (Capsules de départ) */
    div.stButton > button {
        background-color: #171719 !important;
        color: #c4c7c5 !important;
        border: 1px solid #2e3035 !important;
        border-radius: 16px !important;
        padding: 14px 20px !important;
        width: 100% !important;
        text-align: left !important;
        min-height: 70px !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        border-color: #10b981 !important;
        color: #ffffff !important;
        background-color: #1c2d24 !important;
    }
    
    /* Barre d'entrée de texte flottante style Gemini */
    .stChatInputContainer {
        border-radius: 28px !important;
        border: 1px solid #2e3035 !important;
        background-color: #171719 !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #10b981 !important;
    }
    
    /* Masquage des avatars et boites de dialogue par défaut de Streamlit */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INITIALISATION DU MOTEUR & SESSIONS
# ==========================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = "Invité"
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. PANNEAU LATÉRAL GESTIONNAIRE
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #10b981; font-weight: 500;'>☘️ SMO IA</h2>", unsafe_allow_html=True)
    
    if st.button("➕ Nouveau chat", key="clear_session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    
    if st.session_state.authenticated:
        st.markdown(f"👤 Compte : **{st.session_state.user_name}**")
        st.caption("✅ Mode complet débloqué (Médias actifs)")
        if st.button("Se déconnecter", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_name = "Invité"
            st.rerun()
    else:
        st.markdown("### 🔑 Espace Membre")
        with st.expander("Se connecter / S'inscrire"):
            u = st.text_input("Identifiant")
            p = st.text_input("Mot de passe", type="password")
            if st.button("Connexion", use_container_width=True):
                if u and p:
                    st.session_state.authenticated = True
                    st.session_state.user_name = "Loïc LTP"
                    st.rerun()

    st.markdown("---")
    st.caption("⏱️ Historique Récent")

# ==========================================
# 4. TRACÉ DE L'INTERFACE DE DISCUSSION (STYLE GEMINI VISUEL)
# ==========================================
if not st.session_state.messages:
    # Écran de bienvenue minimaliste pur
    st.markdown(f'<div class="gemini-title">Salut {st.session_state.user_name}, commençons</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Rédiger un texte\n\nAide-moi à concevoir un écrit clair et précis", key="b1"):
            st.session_state.messages.append({"role": "user", "content": "Aide-moi à rédiger un texte clair et structuré."})
            st.rerun()
    with col2:
        if st.button("💻 Optimiser un code\n\nNettoyer mon script pour le rendre plus rapide", key="b2"):
            st.session_state.messages.append({"role": "user", "content": "Analyse et optimise mon code informatique."})
            st.rerun()
    with col3:
        if st.button("💡 Idée de business\n\nCréer un plan d action numérique rentable", key="b3"):
            st.session_state.messages.append({"role": "user", "content": "Donne-moi une stratégie pour lancer un business en ligne efficace."})
            st.rerun()
else:
    # Rendu des messages via HTML5/CSS3 sur mesure pour imiter parfaitement Capture d'écran 2026-06-08 155842.png
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 1.5rem; padding-right: 10px;">
                    <div style="background-color: #1e1f22; color: #ffffff; padding: 12px 24px; border-radius: 24px; max-width: 75%; font-family: 'Inter', sans-serif; font-size: 1rem;">
                        {msg["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="display: flex; flex-direction: column; align-items: flex-start; margin-bottom: 2.5rem; padding-left: 10px; font-family: 'Inter', sans-serif;">
                    <div style="color: #f0f4f9; font-size: 1.05rem; line-height: 1.6; max-width: 95%; white-space: pre-wrap;">{msg["content"]}</div>
                    <!-- Ligne d'outils d'actions sous la réponse identique à Gemini -->
                    <div style="display: flex; gap: 16px; color: #80868b; margin-top: 14px; font-size: 0.9rem; cursor: pointer; user-select: none;">
                        <span title="Bonne réponse">👍</span>
                        <span title="Mauvaise réponse">👎</span>
                        <span title="Recommencer">🔄</span>
                        <span title="Copier">📋</span>
                        <span title="Plus">⋯</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 5. ZONE D'ENTRÉE & TRAITEMENT DE LA COMMUNICATION
# ==========================================
if not st.session_state.authenticated:
    st.markdown("<p style='text-align: center; color: #80868b; font-size: 0.85rem; margin-top: 20px;'>💡 Pour insérer vos photos, vos vidéos ou approfondir vos recherches de façon experte, créez un compte dans le panneau latéral.</p>", unsafe_allow_html=True)

# Barre de saisie utilisateur
user_query = st.chat_input("Demander à SMO IA...")

# Traitement de la communication fluide (Ancienne ligne 200 entièrement corrigée)
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.rerun()

# Déclenchement automatique de la réponse si le dernier message vient de l'utilisateur
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    
    # Construction de l'historique complet pour maintenir le fil de la conversation
    historique_complet = [{"role": "system", "content": "Tu es SMO IA, une intelligence artificielle dotée d'une approche humaine et bienveillante. Tu es experte en programmation et business."}]
    for m in st.session_state.messages:
        historique_complet.append({"role": m["role"], "content": m["content"]})
        
    try:
        # Appel direct et fluide de l'API OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=historique_complet,
            temperature=0.7
        )
        reponse_ia = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reponse_ia})
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Désolé, une erreur technique est survenue : {str(e)}"})
        
    st.rerun()

# Mention légale fixe tout en bas de page (Style Capture d'écran 2026-06-08 155830.png)
st.markdown("<div style='position: fixed; bottom: 12px; left: 0; right: 0; text-align: center; color: #80868b; font-size: 0.75rem; font-family: sans-serif;'>SMO IA est une IA et peut se tromper.</div>", unsafe_allow_html=True)
