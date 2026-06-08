import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
load_dotenv()

# =========================================================================
# 1. CONFIGURATION DE LA PAGE & DESIGN SYSTEM COMPLET (VERRE 3D & HALO VERT)
# =========================================================================
st.set_page_config(
    page_title="SMO IA",
    page_icon="☘️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Injection CSS : Effet Verre 3D et dégradé vert tamisé montant depuis le bas
st.markdown("""
    <style>
    /* Fond de l'application : lueur verte émeraude 3D montante et tamisée */
    .stApp {
        background: linear-gradient(to top, rgba(16, 185, 129, 0.15) 0%, rgba(14, 15, 18, 1) 55%) !important;
        background-attachment: fixed !important;
        color: #f0f4f9 !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Masquage des éléments techniques natifs Streamlit */
    header, footer, [data-testid="stDecoration"] {
        visibility: hidden !important;
        height: 0px !important;
    }
    
    /* Barre latérale : Design épuré en verre fumé sombre */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 16, 19, 0.85) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.04) !important;
    }
    
    /* Titre d'accueil principal */
    .smo-main-title {
        font-weight: 500;
        font-size: 2.5rem;
        color: #ffffff;
        text-align: center;
        margin-top: 6rem;
        margin-bottom: 2.5rem;
        letter-spacing: -0.5px;
    }
    
    /* --- STRUCTURE VERRE 3D (GLASSMORPHISM) --- */
    
    /* Boutons et capsules de suggestions en Verre Réactif */
    div.stButton > button {
        background: rgba(35, 37, 41, 0.45) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        color: #c4c7c5 !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 16px !important;
        padding: 14px 20px !important;
        width: 100% !important;
        text-align: left !important;
        min-height: 72px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.08);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }
    
    /* Interaction lumineuse intense au survol de la capsule */
    div.stButton > button:hover {
        border-color: rgba(16, 185, 129, 0.5) !important;
        color: #ffffff !important;
        background: rgba(16, 185, 129, 0.1) !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(16, 185, 129, 0.15), inset 0 1px 1px rgba(255, 255, 255, 0.15);
    }
    
    /* Zone d'écriture flottante : Verre poli haut de gamme */
    .stChatInputContainer {
        border-radius: 28px !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        background: rgba(28, 30, 33, 0.75) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), 0 -4px 20px rgba(16, 185, 129, 0.02) !important;
    }
    .stChatInputContainer:focus-within {
        border-color: rgba(16, 185, 129, 0.6) !important;
    }
    
    /* Neutralisation des blocs de messages par défaut */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0px !important;
    }
    
    /* Alerte d'erreur et guide d'activation stylisé en Verre Ambré/Vert */
    .error-glass-panel {
        background: rgba(16, 185, 129, 0.06) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 20px;
        padding: 24px;
        color: #e0e4e8;
        margin-top: 15px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.05);
    }
    .error-glass-panel ol {
        margin-top: 10px;
        margin-bottom: 10px;
        padding-left: 20px;
    }
    .error-glass-panel li {
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# 2. CONFIGURATION DU MOTEUR GRATUIT GEMINI
# =========================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================================
# 3. BARRE LATÉRALE DE GESTION
# =========================================================================
with st.sidebar:
    st.markdown("<h2 style='color: #10b981; font-weight: 500; font-size: 1.6rem; letter-spacing: -0.5px;'>☘️ SMO IA</h2>", unsafe_allow_html=True)
    
    if st.button("➕ Nouveau chat", key="btn_new_chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("👤 Membre : **Loïc**")
    st.caption("✅ Accès Intégral Libre")
    st.markdown("---")
    st.caption("⏱️ Historique de chat")

# =========================================================================
# 4. ZONE D'AFFICHAGE ET DIALOGUES ÉPURÉS
# =========================================================================
if not st.session_state.messages:
    st.markdown('<div class="smo-main-title">Salut Loïc, commençons</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Rédiger un texte\n\nAide-moi à concevoir un écrit clair et précis", key="sug_1"):
            st.session_state.messages.append({"role": "user", "content": "Aide-moi à rédiger un texte clair et structuré."})
            st.rerun()
    with col2:
        if st.button("💻 Optimiser un code\n\nNettoyer mon script pour le rendre plus rapide", key="sug_2"):
            st.session_state.messages.append({"role": "user", "content": "Analyse et optimise mon code informatique."})
            st.rerun()
    with col3:
        if st.button("💡 Idée de business\n\nCréer un plan d action numérique rentable", key="sug_3"):
            st.session_state.messages.append({"role": "user", "content": "Donne-moi une stratégie pour lancer un business en ligne efficace."})
            st.rerun()
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            # Sécurisation du rendu HTML avec .format() pour éviter les bugs d'f-string
            user_html = """
                <div style="display: flex; justify-content: flex-end; margin-bottom: 1.6rem;">
                    <div style="background: rgba(255, 255, 255, 0.06); color: #ffffff; padding: 12px 24px; border-radius: 22px; max-width: 75%; box-shadow: inset 0 1px 1px rgba(255,255,255,0.08); font-size: 0.98rem;">
                        {}
                    </div>
                </div>
            """.format(msg["content"])
            st.markdown(user_html, unsafe_allow_html=True)
        else:
            # Sécurisation du rendu HTML avec .format() pour éviter les bugs d'f-string
            assistant_html = """
                <div style="margin-bottom: 2.5rem; padding: 0 10px;">
                    <div style="color: #f0f4f9; font-size: 1.02rem; line-height: 1.65; white-space: pre-wrap;">{}</div>
                    <div style="display: flex; gap: 18px; color: #747775; margin-top: 14px; font-size: 0.88rem; user-select: none; cursor: pointer;">
                        <span title="Utile">👍</span> <span title="Pas utile">👎</span> <span title="Régénérer">🔄</span> <span title="Copier le texte">📋</span> <span title="Options">⋯</span>
                    </div>
                </div>
            """.format(msg["content"])
            st.markdown(assistant_html, unsafe_allow_html=True)

# =========================================================================
# 5. ENTRÉE UTILISATEUR ET TRAITEMENT AVEC MOTEUR GEMINI GRATUIT
# =========================================================================
query_input = st.chat_input("Demander à SMO IA...")

if query_input:
    st.session_state.messages.append({"role": "user", "content": query_input})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    
    # SI LA CLÉ EST MANQUANTE : Affichage propre du guide d'activation
    if not GEMINI_API_KEY:
        guide_activation_html = """
        <div class="error-glass-panel">
            <strong style="color: #10b981; font-size: 1.1rem;">🔑 Activation de SMO IA requise (Moteur Gratuit)</strong><br><br>
            Pour contourner définitivement les phases de paiement et utiliser l'application gratuitement, suis ce guide rapide :
            <ol>
                <li>Rends-toi sur la plateforme officielle : <a href="https://aistudio.google.com/" target="_blank" style="color: #10b981; text-decoration: underline; font-weight: bold;">Google AI Studio</a>.</li>
                <li>Connecte-toi simplement à l'aide de ton compte Google habituel.</li>
                <li>Clique sur le bouton bleu <b>"Get API key"</b> situé en haut à gauche, puis sur <b>"Create API key"</b>.</li>
                <li>Sélectionne <b>"Create API key in a new project"</b> et copie la clé générée (elle commence par <code>AIzaSy...</code>).</li>
                <li>Ouvre ton fichier local <code>.env</code> et remplace ou ajoute la ligne suivante :</li>
            </ol>
            <div style="background: rgba(0, 0, 0, 0.4); padding: 12px; border-radius: 8px; font-family: monospace; border: 1px solid rgba(255,255,255,0.05); color: #10b981; margin-top: 5px;">
                GEMINI_API_KEY=colle_ici_ta_cle_recuperee
            </div>
        </div>
        """
        st.session_state.messages.append({"role": "assistant", "content": guide_activation_html})
        st.rerun()
        
    try:
        # Initialisation du modèle gratuit de Google
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="Tu es SMO IA, une intelligence artificielle dotée d'une conscience humaine et bienveillante. Tu es intégrée dans un superbe environnement 3D en verre."
        )
        
        # Adaptation de l'historique pour le format Gemini
        chat_history = []
        for m in st.session_state.messages[:-1]:
            role = "user" if m["role"] == "user" else "model"
            chat_history.append({"role": role, "parts": [m["content"]]})
            
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(st.session_state.messages[-1]["content"])
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": "Erreur système rencontrée : {}".format(str(e))})
        
    st.rerun()
