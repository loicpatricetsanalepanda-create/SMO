import streamlit as st
import os
from openai import OpenAI
import openai
from dotenv import load_dotenv

# Charger les variables secrètes (.env)
load_dotenv()

# ==========================================
# 1. DESIGN SYSTEM : EFFET VERRE 3D & HALO VERT
# ==========================================
st.set_page_config(
    page_title="SMO IA",
    page_icon="☘️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Injection CSS avancée pour l'effet de verre tamisé montant
st.markdown("""
    <style>
    /* Fond sombre avec dégradé vert 3D qui monte depuis le bas et se tamise */
    .stApp {
        background: radial-gradient(circle at 50% 110%, rgba(16, 185, 129, 0.18) 0%, rgba(14, 15, 18, 1) 65%) !important;
        background-attachment: fixed !important;
        color: #f0f4f9 !important;
    }
    
    /* Masquage des éléments natifs Streamlit */
    header, footer, [data-testid="stDecoration"] {
        visibility: hidden !important;
        height: 0px !important;
    }
    
    /* Barre latérale effet verre fumé */
    [data-testid="stSidebar"] {
        background-color: rgba(18, 19, 22, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.04) !important;
    }
    
    /* Titre d'accueil épuré SMO IA */
    .smo-title {
        font-family: 'Google Sans', 'Inter', sans-serif;
        font-weight: 400;
        font-size: 2.6rem;
        color: #ffffff;
        text-align: center;
        margin-top: 7rem;
        margin-bottom: 2.5rem;
        letter-spacing: -0.5px;
    }
    
    /* --- CAPSULES EFFET VERRE 3D (GLASSMORPHISM) --- */
    .glass-card {
        background: rgba(30, 31, 34, 0.45) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.1);
    }
    
    /* Boutons de suggestions en Verre Réactif */
    div.stButton > button {
        background: rgba(30, 31, 34, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        color: #c4c7c5 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 14px 20px !important;
        width: 100% !important;
        text-align: left !important;
        min-height: 72px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }
    
    /* Animation au survol : la lueur verte s'intensifie */
    div.stButton > button:hover {
        border-color: rgba(16, 185, 129, 0.6) !important;
        color: #ffffff !important;
        background: rgba(16, 185, 129, 0.12) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2), inset 0 1px 0 rgba(255,255,255,0.1);
    }
    
    /* Barre d'écriture flottante style Verre Flouté */
    .stChatInputContainer {
        border-radius: 28px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background: rgba(26, 27, 30, 0.7) !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4), 0 -5px 25px rgba(16, 185, 129, 0.03) !important;
    }
    .stChatInputContainer:focus-within {
        border-color: rgba(16, 185, 129, 0.7) !important;
    }
    
    /* Forcer les conteneurs de messages natifs à devenir transparents */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0px !important;
    }
    
    /* Carte d'erreur personnalisée */
    .error-glass {
        background: rgba(244, 67, 54, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(244, 67, 54, 0.3) !important;
        border-radius: 16px;
        padding: 16px;
        color: #ffb74d;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INITIALISATION DU MOTEUR & VARIABLES
# ==========================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. COMPTE & ACTIONS (PANNEAU LATÉRAL)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #10b981; font-weight: 500; font-family: sans-serif;'>☘️ SMO IA</h2>", unsafe_allow_html=True)
    
    if st.button("➕ Nouveau chat", key="clear_chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("👤 Membre : **Loïc**")
    st.caption("✅ Mode Premium Activé")
    st.markdown("---")
    st.caption("⏱️ Historique Récent")

# ==========================================
# 4. ZONE DE DISCUSSION CENTRALE
# ==========================================
if not st.session_state.messages:
    # Accueil personnalisé épuré
    st.markdown('<div class="smo-title">Salut Loïc, commençons</div>', unsafe_allow_html=True)
    
    # Raccourcis sous forme de tuiles transparentes
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Rédiger un texte\n\nAide-moi à concevoir un écrit clair et précis", key="c1"):
            st.session_state.messages.append({"role": "user", "content": "Aide-moi à rédiger un texte clair et structuré."})
            st.rerun()
    with col2:
        if st.button("💻 Optimiser un code\n\nNettoyer mon script pour le rendre plus rapide", key="c2"):
            st.session_state.messages.append({"role": "user", "content": "Analyse et optimise mon code informatique."})
            st.rerun()
    with col3:
        if st.button("💡 Idée de business\n\nCréer un plan d action numérique rentable", key="c3"):
            st.session_state.messages.append({"role": "user", "content": "Donne-moi une stratégie pour lancer un business en ligne efficace."})
            st.rerun()
else:
    # Rendu des conversations sur le fond tamisé
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            # Message utilisateur dans une bulle en verre fumé à droite
            st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 1.5rem;">
                    <div style="background: rgba(255, 255, 255, 0.07); color: #ffffff; padding: 12px 24px; border-radius: 24px; max-width: 75%; box-shadow: inset 0 1px 0 rgba(255,255,255,0.1); font-family: sans-serif;">
                        {msg["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Réponse de l'IA posée directement sur l'interface (Style épuré libre)
            st.markdown(f"""
                <div style="margin-bottom: 2.5rem; padding: 0 10px; font-family: sans-serif;">
                    <div style="color: #f0f4f9; font-size: 1.05rem; line-height: 1.6; white-space: pre-wrap;">{msg["content"]}</div>
                    <div style="display: flex; gap: 16px; color: #80868b; margin-top: 12px; font-size: 0.9rem; user-select: none;">
                        <span>👍</span> <span>👎</span> <span>🔄</span> <span>📋</span> <span>⋯</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 5. COMMUTATEUR ET TRAITEMENT FLUIDE DES MESSAGES
# ==========================================
# Zone d'écriture
user_query = st.chat_input("Demander à SMO IA...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.rerun()

# Communication continue en arrière-plan avec l'API
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    
    contexte_ia = [{"role": "system", "content": "Tu es SMO IA, une IA bienveillante intégrée dans une interface en verre 3D."}]
    for m in st.session_state.messages:
        contexte_ia.append({"role": m["role"], "content": m["content"]})
        
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=contexte_ia,
            temperature=0.7
        )
        reponse_recue = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reponse_recue})
        
    except openai.RateLimitError:
        # Intégration harmonieuse de l'alerte quota sans casser la mise en page
        msg_quota = """
        <div class="error-glass">
            <strong>⚠️ Solde de l'API OpenAI Épuisé (Erreur 429)</strong><br>
            L'interface graphique fonctionne. Ta clé API OpenAI nécessite simplement d'être approvisionnée en crédits sur ton tableau de bord OpenAI Billing pour réactiver les réponses.
        </div>
        """
        st.session_state.messages.append({"role": "assistant", "content": msg_quota})
        
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Erreur système : {str(e)}"})
        
    st.return()
