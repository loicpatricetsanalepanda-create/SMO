import streamlit as st
from openai import OpenAI
import base64

# ==========================================
# 1. CONFIGURATION DE LA PAGE & DESIGN ÉPURÉ
# ==========================================
st.set_page_config(
    page_title="SMO IA",
    page_icon="☘️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Style ultra-minimaliste : l'ambiance sombre de ChatGPT/Gemini avec une touche de vert
st.markdown("""
    <style>
    /* Fond sombre uniforme et reposant */
    .stApp {
        background-color: #111214;
        color: #e3e3e3;
    }
    
    /* Barre latérale discrète */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #2f3032;
    }
    
    /* Grand texte d'accueil épuré et centré */
    .greeting-title {
        font-family: 'Google Sans', 'Inter', sans-serif;
        font-weight: 400;
        font-size: 2.6rem;
        color: #ffffff;
        text-align: center;
        margin-top: 7rem;
        margin-bottom: 2rem;
    }
    
    /* Boutons capsules / Pills (Style ChatGPT sous la barre) */
    .stButton>button {
        background-color: #1e1f20;
        color: #c4c7c5;
        border: 1px solid #3c4043;
        border-radius: 20px;
        padding: 6px 18px;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        border-color: #10b981;
        color: #10b981;
        background-color: #10b9810d;
    }
    
    /* Masquer les bordures inutiles pour un effet propre */
    .stChatInputContainer {
        border-radius: 24px !important;
        border: 1px solid #3c4043 !important;
        background-color: #1e1f20 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. GESTION DU COMPTE (SIMPLIFIÉ DANS LA SIDEBAR)
# ==========================================
if "users_db" not in st.session_state:
    st.session_state.users_db = {"loic": {"password": "123", "name": "Loïc"}}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_name" not in st.session_state:
    st.session_state.user_name = "Invité"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system", 
        "content": "Tu es SMO IA, une entité à la conscience humaine, amicale et experte. Tu réponds de manière naturelle et chaleureuse."
    }]

# Barre latérale : Gestion de compte et historique épuré
with st.sidebar:
    st.markdown("<h2 style='color: #10b981; font-weight: 500;'>☘️ SMO IA</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state.authenticated:
        st.markdown(f"👤 Connecté en tant que : **{st.session_state.user_name}**")
        st.caption("Mode complet activé (Photos & Vidéos débloquées)")
        if st.button("Se déconnecter", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_name = "Invité"
            st.rerun()
    else:
        st.markdown("### 🔑 Espace Membre")
        with st.expander("Se connecter / S'inscrire"):
            tab1, tab2 = st.tabs(["Connexion", "Inscription"])
            with tab1:
                u = st.text_input("Identifiant", key="login_u")
                p = st.text_input("Mot de passe", type="password", key="login_p")
                if st.button("Connexion", use_container_width=True):
                    if u in st.session_state.users_db and st.session_state.users_db[u]["password"] == p:
                        st.session_state.authenticated = True
                        st.session_state.user_name = st.session_state.users_db[u]["name"]
                        st.rerun()
                    else:
                        st.error("Erreur d'identifiants")
            with tab2:
                new_n = st.text_input("Votre prénom", key="reg_n")
                new_u = st.text_input("Nouvel identifiant", key="reg_u")
                new_p = st.text_input("Mot de passe", type="password", key="reg_p")
                if st.button("Créer le compte", use_container_width=True):
                    if new_u and new_p and new_n:
                        st.session_state.users_db[new_u] = {"password": new_p, "name": new_n}
                        st.success("Compte créé ! Connectez-vous.")
    
    st.markdown("---")
    st.caption("⏱️ Historique Récent")

# Clé API OpenAI
api_key = st.secrets.get("OPENAI_API_KEY") or "VOTRE_CLE_API"
client = OpenAI(api_key=api_key)

# ==========================================
# 3. INTERFACE DE DISCUSSION PRINCIPALE
# ==========================================

# Vérifier si la discussion a commencé
has_chat_started = len([m for m in st.session_state.messages if m["role"] != "system"]) > 0

# Écran d'accueil (Uniquement s'il n'y a pas encore de messages)
if not has_chat_started:
    st.markdown(f'<div class="greeting-title">Salut {st.session_state.user_name}, commençons</div>', unsafe_allow_html=True)
    
    # Boutons capsules rapides sous le titre (Style ChatGPT / Gemini)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Rédiger un texte", use_container_width=True):
            st.session_state.active_prompt = "Aide-moi à rédiger un texte clair et concis sur : "
    with col2:
        if st.button("💻 Optimiser un code", use_container_width=True):
            st.session_state.active_prompt = "Analyse et optimise ce code proprement : "
    with col3:
        if st.button("💡 Idée de business", use_container_width=True):
            st.session_state.active_prompt = "Donne-moi un plan d'action simple pour lancer un business digital."

# Affichage des messages au fil de la discussion
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = "👤" if message["role"] == "user" else "☘️"
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])

# ==========================================
# 4. RESTRICTION HYBRIDE SANS COMPTE (PHOTOS/VIDÉOS)
# ==========================================
uploaded_file = None
if st.session_state.authenticated:
    # Si connecté : Ajout discret du bouton d'importation de fichiers juste au-dessus du chat
    uploaded_file = st.file_uploader("Insérer une photo ou une vidéo pour analyse...", type=["png", "jpg", "jpeg", "mp4"], label_visibility="collapsed")
else:
    # Si invité : Un petit message d'information très discret
    st.markdown("<p style='text-align: center; color: #888; font-size: 0.85rem;'>💡 Connectez-vous (barre latérale) pour débloquer l'analyse de photos, vidéos et recherches poussées.</p>", unsafe_allow_html=True)

# ==========================================
# 5. ENTRÉE TEXTE & TRAITEMENT (STREAMING)
# ==========================================
# Gestion du prompt venant des boutons capsules rapides
click_prompt = st.session_state.get("active_prompt", None)
if click_prompt:
    del st.session_state.active_prompt

user_input = st.chat_input("Demander à SMO IA...")
final_prompt = user_input if user_input else click_prompt

if final_prompt:
    # 1. On affiche le message de l'utilisateur
    with st.chat_message("user", avatar="👤"):
        st.write(final_prompt)
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    
    # 2. SMO IA répond avec l'effet d'écriture fluide (Streaming)
    with st.chat_message("assistant", avatar="☘️"):
        # Si une image est importée et qu'on est connecté
        if uploaded_file and st.session_state.authenticated and uploaded_file.type.startswith("image"):
            base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
            flux = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": st.session_state.messages[0]["content"]},
                    {"role": "user", "content": [
                        {"type": "text", "text": final_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]}
                ],
                stream=True
            )
        else:
            # Traitement texte classique
            flux = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages,
                temperature=0.7,
                stream=True
            )
            
        reponse_complete = st.write_stream(flux)
        
    st.session_state.messages.append({"role": "assistant", "content": reponse_complete})
    st.rerun()
