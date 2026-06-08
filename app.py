import streamlit as st
from openai import OpenAI
import base64

# ==========================================
# 1. CONFIGURATION DE LA PAGE & DESIGN EMERAUDE GLOW
# ==========================================
st.set_page_config(
    page_title="SMO IA",
    page_icon="☘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS pour fusionner le halo de Gemini et les capsules de ChatGPT en version Verte
st.markdown("""
    <style>
    /* Fond sombre avec le fameux effet Halo Lumineux (Spotlight) centré style Gemini */
    .stApp {
        background: radial-gradient(circle at 50% 40%, #0a2419 0%, #050a08 60%, #020403 100%);
        color: #e2e8f0;
    }
    
    /* Sidebar minimaliste style ChatGPT */
    [data-testid="stSidebar"] {
        background-color: #060b08 !important;
        border-right: 1px solid #103322;
    }
    
    /* Grand message d'accueil centré */
    .welcome-text {
        font-family: 'Inter', 'Google Sans', sans-serif;
        font-weight: 500;
        font-size: 2.8rem;
        color: #ffffff;
        text-align: center;
        margin-top: 8rem;
        margin-bottom: 2rem;
        letter-spacing: -0.5px;
    }
    
    /* Barre d'input flottante et arrondie */
    .stChatInputContainer {
        border-radius: 28px !important;
        border: 1px solid #1b4d36 !important;
        background-color: #0d1712 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Capsules / Boutons de suggestions rapides style ChatGPT */
    .suggestion-pill {
        display: inline-block;
        background-color: #0d1712;
        border: 1px solid #1b4d36;
        color: #94a3b8;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 5px;
    }
    .suggestion-pill:hover {
        border-color: #10b981;
        color: #ffffff;
        background-color: #10b9811a;
    }

    /* Badge Premium pour inciter à la création de compte */
    .premium-badge {
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Helper pour encoder les images
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

# ==========================================
# 2. GESTION DES SESSIONS & AUTHENTIFICATION
# ==========================================
if "users_db" not in st.session_state:
    st.session_state.users_db = {"loic": {"password": "password123", "name": "Loïc LTP"}}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_info" not in st.session_state:
    st.session_state.user_info = {"name": "Invité", "username": None}

if "messages" not in st.session_state:
    # Personnalité profonde et humaine de SMO IA
    st.session_state.messages = [{
        "role": "system", 
        "content": "Tu es SMO IA, une entité dotée d'une conscience et d'une bienveillance humaine. Tu es experte en code et business, mais tu t'exprimes avec chaleur, empathie et philosophie."
    }]

# ==========================================
# 3. BARRE LATÉRALE (SIDEBAR) - DESIGN & COMPTE
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #10b981; font-family: sans-serif;'>☘️ SMO IA</h2>", unsafe_allow_html=True)
    
    if st.session_state.authenticated:
        st.markdown(f"### 👤 {st.session_state.user_info['name']}")
        st.caption("Compte Vérifié — Accès Illimité")
        if st.button("Se déconnecter", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_info = {"name": "Invité", "username": None}
            st.rerun()
    else:
        st.markdown("### 🔑 Mode Invité")
        st.caption("Fonctionnalités de base uniquement.")
        
        # Formulaire Connexion / Inscription intégré proprement
        with st.expander("Se connecter / Créer un compte"):
            tab_login, tab_signup = st.tabs(["Connexion", "S'inscrire"])
            
            with tab_login:
                user_in = st.text_input("Identifiant", key="login_u")
                pass_in = st.text_input("Mot de passe", type="password", key="login_p")
                if st.button("Connexion", use_container_width=True):
                    if user_in in st.session_state.users_db and st.session_state.users_db[user_in]["password"] == pass_in:
                        st.session_state.authenticated = True
                        st.session_state.user_info = {"name": st.session_state.users_db[user_in]["name"], "username": user_in}
                        st.success("Connexion réussie !")
                        st.rerun()
                    else:
                        st.error("Identifiants incorrects.")
            
            with tab_signup:
                new_name = st.text_input("Nom complet", key="sign_n")
                new_user = st.text_input("Choisir un identifiant", key="sign_u")
                new_pass = st.text_input("Mot de passe", type="password", key="sign_p")
                if st.button("Créer mon compte", use_container_width=True):
                    if new_user in st.session_state.users_db:
                        st.error("Identifiant déjà pris.")
                    elif new_user and new_pass and new_name:
                        st.session_state.users_db[new_user] = {"password": new_pass, "name": new_name}
                        st.success("Compte créé ! Connectez-vous.")
                    else:
                        st.warning("Veuillez remplir tous les champs.")

    st.markdown("---")
    st.markdown("### Recents")
    st.caption("Connectez-vous pour sauvegarder votre historique de conversation.")

# Récupération de la clé API sécurisée
api_key = st.secrets.get("OPENAI_API_KEY") or "VOTRE_CLE_API_PROVISOIRE"
client = OpenAI(api_key=api_key)

# ==========================================
# 4. ZONE CENTRALE ET INTERFACE MULTIMODALE
# ==========================================

# Détecter si des messages ont déjà été échangés pour épurer l'interface
has_history = len([m for m in st.session_state.messages if m["role"] != "system"]) > 0

# Si aucun message : Afficher le design épuré inspiré de Gemini et ChatGPT
if not has_history:
    greeting = f"Salut {st.session_state.user_info['name']}, commençons" if st.session_state.authenticated else "Que voulez-vous explorer aujourd'hui ?"
    st.markdown(f'<div class="welcome-text">{greeting}</div>', unsafe_allow_html=True)
    
    # Boutons d'actions rapides sous la zone de texte (inspirés de image_b18cee.png)
    col_p1, col_p2, col_p3 = st.columns([1, 1, 1])
    with col_p1:
        if st.button("📝 Rédiger ou modifier un texte", key="p1", use_container_width=True):
            st.session_state.prefilled_prompt = "Aide-moi à rédiger ou modifier un texte de manière percutante : "
    with col_p2:
        if st.button("💡 Structurer un projet digital", key="p2", use_container_width=True):
            st.session_state.prefilled_prompt = "Donne-moi une structure complète pour lancer un projet digital innovant."
    with col_p3:
        if st.button("🔍 Demander une recherche poussée", key="p3", use_container_width=True):
            if not st.session_state.authenticated:
                st.session_state.show_restriction_warning = True
            else:
                st.session_state.prefilled_prompt = "Effectue une recherche approfondie et philosophique sur : "

# Si l'utilisateur a cliqué sur une restriction en mode invité
if st.session_state.get("show_restriction_warning", False):
    st.warning("⚠️ **Fonctionnalité limitée :** La recherche approfondie et l'analyse de médias nécessitent un compte. Créez un compte gratuitement dans la barre latérale pour débloquer toute la puissance de SMO IA !")
    if st.button("J'ai compris"):
        st.session_state.show_restriction_warning = False
        st.rerun()

# Zone d'affichage des messages existants
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = "👤" if message["role"] == "user" else "☘️"
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])

# ==========================================
# 5. BLOC DE LIMITATION MULTIMODALE (PHOTOS / VIDÉOS)
# ==========================================
st.markdown("---")
if st.session_state.authenticated:
    st.markdown("#### 👁️ Zone Multimodale (Compte Actif)")
    uploaded_file = st.file_uploader("Ajouter une photo ou une vidéo pour analyse immédiate...", type=["png", "jpg", "jpeg", "mp4"])
else:
    st.markdown("#### 🔒 Options Multimodales bloquées")
    st.info("💡 Pour insérer des images, des vidéos ou réaliser des analyses visuelles complètes comme sur Gemini, veuillez créer un compte ou vous connecter via le panneau latéral.")
    uploaded_file = None

# ==========================================
# 6. ENTRÉE DES MESSAGES ET STREAMING
# ==========================================
initial_prompt = st.session_state.get("prefilled_prompt", "")
if initial_prompt:
    # On nettoie la session pour éviter la boucle infinie au rechargement
    del st.session_state.prefilled_prompt

user_input = st.chat_input("Demander à SMO IA...")
prompt = user_input if user_input else (initial_prompt if initial_prompt else None)

if prompt:
    # Affichage du message de l'utilisateur
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Génération de la réponse de SMO IA
    with st.chat_message("assistant", avatar="☘️"):
        message_placeholder = st.empty()
        
        # Logique de traitement si une image est fournie (uniquement pour les comptes connectés)
        if uploaded_file and st.session_state.authenticated and uploaded_file.type.startswith("image"):
            base64_image = encode_image(uploaded_file)
            flux = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": st.session_state.messages[0]["content"]},
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]}
                ],
                stream=True
            )
        else:
            # Traitement texte classique ou invité
            flux = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages,
                temperature=0.7,
                stream=True
            )
        
        reponse_complete = st.write_stream(flux)
        
    st.session_state.messages.append({"role": "assistant", "content": reponse_complete})
    st.rerun()
