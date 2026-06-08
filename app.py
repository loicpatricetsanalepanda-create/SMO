import streamlit as st
import os
from openai import OpenAI
import openai
from dotenv import load_dotenv

# Charger les variables secrètes (.env)
load_dotenv()

# ==========================================
# 1. DESIGN SYSTEM ULTRA-FIDÈLE (STYLE CHATGPT)
# ==========================================
st.set_page_config(
    page_title="SMO IA",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Injection CSS avancée pour calquer l'interface de ChatGPT (Captures 151700 / 160153)
st.markdown("""
    <style>
    /* Fond noir mat absolu de ChatGPT */
    .stApp {
        background-color: #212121 !important;
        color: #ececf1 !important;
    }
    
    /* Masquage total des éléments superflus de Streamlit */
    header, footer, [data-testid="stDecoration"] {
        visibility: hidden !important;
        height: 0px !important;
    }
    
    /* Transformation de la Sidebar en barre d'icônes minimaliste noire */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #2f2f2f !important;
        min-width: 80px !important;
        max-width: 90px !important;
    }
    
    /* Conteneur d'icônes personnalisé style ChatGPT dans la barre latérale */
    .chatgpt-sidebar-menu {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 30px;
        margin-top: 20px;
        height: 80vh;
        position: relative;
    }
    
    .sidebar-icon {
        color: #b4b4b4;
        font-size: 1.5rem;
        cursor: pointer;
        transition: color 0.2s;
    }
    .sidebar-icon:hover {
        color: #ffffff;
    }
    
    /* Bouton utilisateur circulaire "LL" rouge tout en bas */
    .avatar-user-ll {
        background-color: #ab47bc !important; /* Couleur pourpre/rouge de la capture */
        color: white !important;
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.9rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Titre d'accueil épuré de ChatGPT */
    .chatgpt-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 2.2rem;
        color: #ffffff;
        text-align: center;
        margin-top: 8rem;
        margin-bottom: 2rem;
        letter-spacing: -0.5px;
    }
    
    /* Boutons de suggestions (Pillules fines avec bordure) */
    div.stButton > button {
        background-color: transparent !important;
        color: #b4b4b4 !important;
        border: 1px solid #4d4d4d !important;
        border-radius: 20px !important;
        padding: 8px 18px !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        border-color: #8e8e93 !important;
        color: #ffffff !important;
        background-color: #2f2f2f !important;
    }
    
    /* Barre d'entrée de texte flottante de ChatGPT (Arrondie et sombre) */
    .stChatInputContainer {
        border-radius: 26px !important;
        border: 1px solid #4d4d4d !important;
        background-color: #2f2f2f !important;
    }
    
    /* Message d'erreur personnalisé style Premium */
    .error-card {
        background-color: #2a1a1a;
        border: 1px solid #f44336;
        border-radius: 12px;
        padding: 16px;
        margin: 15px 0;
        color: #ff9800;
        font-family: 'Inter', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INITIALISATION DES MOTEURS & SESSIONS
# ==========================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. BARRE LATÉRALE RE-DESIGNÉE (STYLE CHATGPT)
# ==========================================
with st.sidebar:
    # Structure HTML/Widgets pour correspondre à Capture d'écran 2026-06-08 160153.png
    st.markdown("""
        <div style="text-align: center; margin-bottom: 25px;">
            <span style="font-size: 1.8rem; color: white;">⚡</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📝", key="new_chat_icon", help="Nouveau chat"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("<br><div style='text-align:center; color:#666;'>🔍</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#666;'>💬</div>", unsafe_allow_html=True)
    
    # Remplir l'espace pour pousser le profil vers le bas
    st.markdown("<div style='height: 50vh;'></div>", unsafe_allow_html=True)
    
    # Pastille ronde "LL" en bas de la barre latérale
    st.markdown('<div class="avatar-user-ll">LL</div>', unsafe_allow_html=True)

# ==========================================
# 4. ZONE DE TEXTE CENTRALE (QU'EST-CE QUI VOUS INTÉRESSE...)
# ==========================================
if not st.session_state.messages:
    # Titre calqué sur ta capture d'écran
    st.markdown('<div class="chatgpt-title">Qu\'est-ce qui vous intéresse aujourd\'hui ?</div>', unsafe_allow_html=True)
    
    # Alignement horizontal des pillules de choix rapides
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🖼️ Créer une image", key="p1", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Génère-moi une illustration créative."})
            st.rerun()
    with col2:
        if st.button("✏️ Rédiger ou modifier", key="p2", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Aide-moi à rédiger un document officiel."})
            st.rerun()
    with col3:
        if st.button("🌐 Faire une recherche", key="p3", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Fais une recherche approfondie sur le web."})
            st.rerun()
else:
    # Flux des dialogues épurés
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 1.5rem;">
                    <div style="background-color: #2f2f2f; color: #ffffff; padding: 10px 20px; border-radius: 20px; max-width: 75%;">
                        {msg["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Réponse brute sans boite grise, posée directement sur le fond noir
            st.markdown(f"""
                <div style="margin-bottom: 2rem; padding-left: 5px;">
                    <div style="color: #ececf1; font-size: 1rem; line-height: 1.6; white-space: pre-wrap;">{msg["content"]}</div>
                    <div style="display: flex; gap: 14px; color: #7d7d7d; margin-top: 10px; font-size: 0.85rem; user-select: none;">
                        <span>👍</span> <span>👎</span> <span>📋</span> <span>🔄</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 5. BARRE D'ÉCRITURE & GESTION DE L'ERREUR 429 QUOTA
# ==========================================
user_query = st.chat_input("Poser une question...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.rerun()

# Calcul et communication avec l'API
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    
    context_build = [{"role": "system", "content": "Tu es SMO IA, configuré sous une interface type ChatGPT."}]
    for m in st.session_state.messages:
        context_build.append({"role": m["role"], "content": m["content"]})
        
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=context_build,
            temperature=0.7
        )
        reponse_ia = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reponse_ia})
        
    except openai.RateLimitError:
        # Interception propre de l'erreur 429 Quota épuisé
        error_msg = """
        <div class="error-card">
            <strong>⚠️ Solde de l'API OpenAI Épuisé (Erreur 429)</strong><br>
            Ton code fonctionne à merveille ! Cependant, ta clé API OpenAI n'a pas de provision financière active ou a expiré.<br><br>
            <strong>Pour résoudre cela :</strong><br>
            1. Rends-toi sur <a href="https://platform.openai.com/settings/organization/billing" target="_blank" style="color: #ff9800; text-decoration: underline;">OpenAI Billing</a>.<br>
            2. Ajoute un minimum de 5$ de crédit sur ton compte (Prepaid Funds).
        </div>
        """
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Une erreur imprévue est survenue : {str(e)}"})
        
    st.rerun()
