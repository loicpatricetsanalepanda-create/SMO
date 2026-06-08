import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Charger les clés secrètes (.env)
load_dotenv()

# ==========================================
# 1. ARCHITECTURE DESIGN SYSTEM (HTML5 & CSS3)
# ==========================================
st.set_page_config(
    page_title="SMO IA",
    page_icon="☘️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Injection d'un système de design propriétaire pour SMO IA (Animations fluides & Éléments épurés)
st.markdown("""
    <style>
    /* Thème de fond Deep Charcoal uniforme */
    .stApp {
        background-color: #111214 !important;
        color: #e3e3e3 !important;
    }
    
    /* Nettoyage complet des éléments natifs pour un rendu épuré pro */
    header, footer, [data-testid="stDecoration"] {
        visibility: hidden !important;
        height: 0px !important;
    }
    
    /* Barre latérale au design lissé */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #2f3032 !important;
    }
    
    /* --- INSPIRATION NEURAL EXPRESSIVE : ANIMATIONS & TYPOGRAPHIE --- */
    
    /* Animation de fondu fluide pour l'apparition des éléments */
    @keyframes smoothFadeUp {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Titre d'accueil minimaliste centré */
    .expressive-title {
        font-family: 'Inter', 'Google Sans', sans-serif;
        font-weight: 400;
        font-size: 2.5rem;
        color: #ffffff;
        text-align: center;
        margin-top: 5rem;
        margin-bottom: 2.5rem;
        letter-spacing: -0.5px;
        animation: smoothFadeUp 0.6s ease-out;
    }
    
    /* Boutons Capsules Tactiles (Micro-interactions au survol) */
    div.stButton > button {
        background-color: #1e1f20 !important;
        color: #c4c7c5 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 16px !important;
        padding: 14px 20px !important;
        width: 100% !important;
        text-align: left !important;
        min-height: 72px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        animation: smoothFadeUp 0.8s ease-out;
    }
    
    /* Effet expressif vert émeraude au survol */
    div.stButton > button:hover {
        border-color: #10b981 !important;
        color: #ffffff !important;
        background-color: #1a2e24 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
    }
    
    /* Barre de recherche arrondie et flottante en bas de page */
    .stChatInputContainer {
        border-radius: 28px !important;
        border: 1px solid #3c4043 !important;
        background-color: #1e1f20 !important;
        transition: border-color 0.2s ease !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #10b981 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INITIALISATION DE L'ENGINE (OPENAI)
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
# 3. INTERFACE COMPTE HYBRIDE (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #10b981; font-weight: 500; font-size: 1.5rem; margin-bottom: 20px;'>☘️ SMO IA</h2>", unsafe_allow_html=True)
    
    if st.button("➕ Nouveau chat", key="nav_new_chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    
    if st.session_state.authenticated:
        st.markdown(f"👤 Compte : **{st.session_state.user_name}**")
        st.caption("✅ Mode complet activé (Images, Vidéos & Recherches poussées)")
        if st.button("Se déconnecter", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_name = "Invité"
            st.rerun()
    else:
        st.markdown("### 🔑 Accès Membre")
        with st.expander("Créer un compte / Connexion"):
            u = st.text_input("Identifiant")
            p = st.text_input("Mot de passe", type="password")
            if st.button("Se connecter", use_container_width=True):
                if u and p:
                    st.session_state.authenticated = True
                    st.session_state.user_name = "Loïc LTP"
                    st.rerun()

    st.markdown("---")
    st.caption("⏱️ Historique Récent")

# ==========================================
# 4. RENDU VISUEL CENTRAL
# ==========================================
if not st.session_state.messages:
    # Écran de présentation épuré utilisant notre feuille de style expressive
    st.markdown(f'<div class="expressive-title">Salut {st.session_state.user_name}, commençons</div>', unsafe_allow_html=True)
    
    # Grille HTML5 de suggestions rapides sous forme de capsules interactives
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Rédiger un texte\n\nAide-moi à concevoir un écrit clair et précis", key="capsule_1"):
            st.session_state.messages.append({"role": "user", "content": "Aide-moi à rédiger un texte clair et structuré."})
            st.rerun()
    with col2:
        if st.button("💻 Optimiser un code\n\nNettoyer mon script pour le rendre plus rapide", key="capsule_2"):
            st.session_state.messages.append({"role": "user", "content": "Analyse et optimise mon code informatique."})
            st.rerun()
    with col3:
        if st.button("💡 Idée de business\n\nCréer un plan d action numérique rentable", key="capsule_3"):
            st.session_state.messages.append({"role": "user", "content": "Donne-moi une stratégie pour lancer un business en ligne efficace."})
            st.rerun()
else:
    # Flux continu des messages de la discussion en cours
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "☘️"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

# ==========================================
# 5. INTÉGRATION DE LA BARRE DE CHAT DIRECTE
# ==========================================
# Note d'information contextuelle si l'utilisateur utilise l'IA sans compte
if not st.session_state.authenticated:
    st.markdown("<p style='text-align: center; color: #80868b; font-size: 0.85rem; margin-top: 25px;'>💡 Pour insérer vos photos, vos vidéos ou approfondir vos recherches de façon experte, créez un compte dans le panneau latéral.</p>", unsafe_allow_html=True)

# Capturer l'action d'écriture de l'utilisateur
user_query = st.chat_input("Demander à SMO IA...")

# Traitement dynamique du signal
if user_query or (st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and len(st.session_state.messages) == 1):
    
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.rerun()

    # Affichage instantané du message envoyé
    with st.chat_message("user", avatar="👤"):
        st.write(st.session_state.messages[-1]["content"])
        
    # Émission en flux continu (Streaming) de la réponse de l'IA
    with st.chat_message("assistant", avatar="☘️"):
        # Déclaration de la personnalité système de SMO IA
        conversation_context = [{"role": "system", "content": "Tu es SMO IA, une intelligence artificielle dotée d'une approche humaine, bienveillante et hautement compétente en développement et en entrepreneuriat numérique."}]
        for m in st.session_state.messages:
            conversation_context.append({"role": m["role"], "content": m["content"]})
            
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation_context,
            temperature=0.7,
            stream=True
        )
        final_response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": final_response})
    st.rerun()

```
