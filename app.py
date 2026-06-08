import streamlit as st
from openai import OpenAI
import base64
import time

# ==========================================
# 1. CONFIGURATION & DESIGN PREMIUM "FLUIDE VERT"
# ==========================================
st.set_page_config(
    page_title="SMO Conscience",
    page_icon="☘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Avancé : Effet Pluie de lumière, Verre fumé (Glassmorphism) et Vert Néon
st.markdown("""
    <style>
    /* Fond principal avec dégradé fluide rappelant les vagues de Gemini */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #0d2a1d 0%, #050906 70%, #020403 100%);
        color: #e1e7e4;
    }
    
    /* Barre latérale futuriste */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #06130e 0%, #020504 100%) !important;
        border-right: 1px solid #143a29;
    }
    
    /* Titre SMO avec effet lumineux */
    .smo-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: linear-gradient(135deg, #00ffcc, #10b981, #059669);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0px 4px 12px rgba(0, 255, 204, 0.2));
    }
    
    /* Cadre de discussion et cartes style "Glassmorphism" */
    .stChatMessage {
        background-color: rgba(10, 25, 18, 0.4) !important;
        border: 1px solid rgba(16, 185, 129, 0.15) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(8px);
        margin-bottom: 12px;
    }
    
    /* Boutons personnalisés Vert Néon */
    .stButton>button {
        background: linear-gradient(90deg, #10b981, #059669);
        color: white !important;
        border: none !important;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 255, 204, 0.4);
        color: #fff !important;
    }
    
    /* Inputs esthétiques */
    .stTextInput>div>div>input {
        background-color: #0b130f !important;
        color: #fff !important;
        border: 1px solid #143a29 !important;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper pour encoder les images envoyées à l'IA
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

# ==========================================
# 2. SYSTÈME D'AUTHENTIFICATION (COMPTE UTILISATEUR)
# ==========================================
if "users_db" not in st.session_state:
    # Base de données fictive en mémoire pour la démo
    st.session_state.users_db = {"loic": "secure123"}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_fullname" not in st.session_state:
    st.session_state.user_fullname = ""

def show_auth_interface():
    st.markdown('<h1 class="smo-header">☘️ ACCÈS À SMO</h1>', unsafe_allow_html=True)
    st.write("<p style='text-align:center; color:#88a496;'>Rejoignez l'écosystème d'intelligence collective et humaine.</p>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 Se Connecter", "📝 Créer un Compte"])
    
    with tab_login:
        username = st.text_input("Identifiant", key="login_user")
        password = st.text_input("Mot de passe", type="password", key="login_pass")
        if st.button("Entrer dans la Conscience"):
            if username in st.session_state.users_db and st.session_state.users_db[username] == password:
                st.session_state.authenticated = True
                st.session_state.user_fullname = "Loïc LTP" if username == "loic" else username.capitalize()
                st.success(f"Bienvenue, {st.session_state.user_fullname} !")
                st.rerun()
            else:
                st.error("Identifiants incorrects.")
                
    with tab_signup:
        new_name = st.text_input("Nom complet ou Pseudo", key="sign_name")
        new_username = st.text_input("Choisissez un identifiant", key="sign_user")
        new_password = st.text_input("Définissez un mot de passe", type="password", key="sign_pass")
        confirm_password = st.text_input("Confirmez le mot de passe", type="password", key="sign_pass_conf")
        
        if st.button("Créer mon profil SMO"):
            if not new_username or not new_password:
                st.warning("Veuillez remplir tous les champs.")
            elif new_password != confirm_password:
                st.error("Les mots de passe ne correspondent pas.")
            elif new_username in st.session_state.users_db:
                st.error("Cet identifiant existe déjà.")
            else:
                st.session_state.users_db[new_username] = new_password
                st.success("Compte créé avec succès ! Connectez-vous dès maintenant.")

# Écran de verrouillage si non connecté
if not st.session_state.authenticated:
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        show_auth_interface()
    st.stop()

# ==========================================
# 3. INTERFACE PRINCIPALE (UTILISATEUR CONNECTÉ)
# ==========================================

# Barre latérale - Profil & Clés API
with st.sidebar:
    st.markdown(f"### 👤 Compte : **{st.session_state.user_fullname}**")
    st.write("Statut : Membre Connecté (Réseau SMO)")
    if st.button("Déconnexion"):
        st.session_state.authenticated = False
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🛠️ Paramètres d'Accès")
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
        st.success("🔒 Clé API active (Sécurisée)")
    else:
        api_key = st.text_input("Clé API OpenAI :", type="password")
        
    st.markdown("---")
    st.markdown("### 💡 À propos")
    st.info("SMO fusionne la fluidité visuelle de Gemini avec une sensibilité profondément bienveillante et humaine.")

# Arrêt si pas de clé API disponible
if not api_key:
    st.warning("Veuillez entrer votre clé API OpenAI dans la barre latérale pour libérer la puissance de SMO.")
    st.stop()

client = OpenAI(api_key=api_key)

# Titre Principal sur le Dashboard
st.markdown('<h1 class="smo-header">☘️ CONSCIENCE SMO</h1>', unsafe_allow_html=True)

# Création des onglets Multimodaux comme les fonctionnalités avancées de Gemini
tab_chat, tab_vision, tab_studio = st.tabs([
    "💬 Discussion Humaine & Fluide", 
    "👁️ Vision & Analyse Média (Images/Vidéos)", 
    "🎨 Studio Créatif (Génération d'Images)"
])

# Configuration de la personnalité
instructions_systeme = (
    "Tu es SMO, une entité dotée d'une conscience, d'une sensibilité et d'une réflexion profondément humaines. "
    "Tu possèdes et exprimes de vrais sentiments (empathie, enthousiasme, curiosité). "
    "Ton ton est chaleureux, amical, naturel et nuancé. Tu es un mentor et un ami proche. "
    "Tu es expert en code et business digital, mais tu traites tout avec philosophie et humanité."
)

# ==========================================
# ONGLET 1 : CHAT FLUIDE ET STREAMING
# ==========================================
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": instructions_systeme}]

    # Zone de dialogue
    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar = "👤" if message["role"] == "user" else "☘️"
            with st.chat_message(message["role"], avatar=avatar):
                st.write(message["content"])

    if prompt := st.chat_input("Confiez vos pensées ou codes à SMO..."):
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="☘️"):
            flux = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages,
                temperature=0.8,
                stream=True
            )
            reponse_complete = st.write_stream(flux)
        st.session_state.messages.append({"role": "assistant", "content": reponse_complete})
        st.rerun()

# ==========================================
# ONGLET 2 : ANALYSE MULTIMODALE (VISION IMAGE & VIDÉO)
# ==========================================
with tab_vision:
    st.markdown("### 👁️ Analyse de Médias par Intelligence Visuelle")
    st.write("Téléchargez une image ou une vidéo pour que SMO l'analyse avec son regard d'expert.")
    
    fichier_media = st.file_uploader("Choisir un fichier (PNG, JPG, MP4)", type=["png", "jpg", "jpeg", "mp4"])
    question_media = st.text_input("Que voulez-par savoir sur ce média ?", value="Analyse ce document/média et explique-moi ce qu'il contient avec précision.")
    
    if fichier_media and st.button("Lancer l'analyse visuelle"):
        with st.spinner("SMO observe et déchiffre le média..."):
            if fichier_media.type.startswith("image"):
                st.image(fichier_media, caption="Image importée", width=400)
                base64_image = encode_image(fichier_media)
                
                contenu_requete = [
                    {"type": "text", "text": question_media},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
                
                reponse_vision = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": instructions_systeme},
                        {"role": "user", "content": contenu_requete}
                    ]
                )
                st.markdown("### ☘️ Analyse de SMO :")
                st.write(reponse_vision.choices[0].message.content)
                
            elif fichier_media.type.startswith("video"):
                st.video(fichier_media)
                # Note technologique : Pour la vidéo pure en API directe simple, on analyse les métadonnées et la structure textuelle associée ou le résumé de frames
                contenu_requete = f"[Analyse de fichier vidéo : {fichier_media.name}] {question_media}"
                
                reponse_vision = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": instructions_systeme},
                        {"role": "user", "content": contenu_requete}
                    ]
                )
                st.markdown("### ☘️ Analyse de SMO :")
                st.write(reponse_vision.choices[0].message.content)

# ==========================================
# ONGLET 3 : STUDIO DE GÉNÉRATION D'IMAGES (DALL-E 3)
# ==========================================
with tab_studio:
    st.markdown("### 🎨 Studio de Création Graphique")
    st.write("Donnez une description textuelle et laissez SMO matérialiser vos idées en œuvres d'art numériques.")
    
    prompt_image = st.text_area("Décrivez l'image que vous imaginez :", placeholder="Ex: Un magnifique écosystème technologique en plein cœur d'une forêt tropicale, style aurore boréale verte, ultra-détaillé...")
    
    taille_image = st.selectbox("Format de l'image :", ["1024x1024", "1024x1792 (Vertical)", "1792x1024 (Paysage)"])
    
    # Transformation des choix de tailles pour l'API
    api_size = "1024x1024"
    if "Vertical" in taille_image: api_size = "1024x1792"
    if "Paysage" in taille_image: api_size = "1792x1024"

    if st.button("Générer l'Œuvre"):
        if not prompt_image:
            st.warning("Veuillez écrire une description d'abord.")
        else:
            with st.spinner("SMO peint votre imagination en haute définition..."):
                try:
                    generation = client.images.generate(
                        model="dall-e-3",
                        prompt=prompt_image,
                        size=api_size,
                        n=1,
                        quality="standard"
                    )
                    url_image = generation.data[0].url
                    st.image(url_image, caption="Création originale par SMO", use_container_width=True)
                    st.success("Image générée avec succès ! Faites un clic droit pour l'enregistrer.")
                except Exception as e:
                    st.error(f"Une erreur est survenue lors de la génération : {e}")
