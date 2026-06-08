import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
from dotenv import load_dotenv

# Charger la clé secrète depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Récupération sécurisée et masquée de la clé
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# ==========================================
# INTERFACE DE DESIGN PREMIUM (Style ChatGPT & Gemini)
# ==========================================
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMO IA</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #111214; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: #2f3032; border-radius: 10px; }
    </style>
</head>
<body class="text-[#e3e3e3] h-screen flex overflow-hidden">

    <!-- BARRE LATÉRALE -->
    <div class="w-64 bg-[#1e1f20] border-r border-[#2f3032] flex flex-col justify-between p-4 hidden md:flex">
        <div>
            <div class="flex items-center space-x-2 text-[#10b981] font-semibold text-xl mb-8">
                <span>☘️</span>
                <span>SMO IA</span>
            </div>
            <button onclick="resetChat()" class="w-full text-left bg-[#111214] border border-[#3c4043] hover:border-[#10b981] text-sm py-2.5 px-4 rounded-xl transition duration-200">
                + Nouveau chat
            </button>
            <div class="mt-6">
                <p class="text-xs text-[#9e9e9e] uppercase font-semibold tracking-wider px-2">Récents</p>
                <div class="mt-2 space-y-1 text-sm text-[#c4c7c5]">
                    <div class="px-2 py-1.5 hover:bg-[#2f3032] rounded-lg cursor-pointer truncate">Discussion générale</div>
                </div>
            </div>
        </div>
        
        <div class="border-t border-[#2f3032] pt-4 flex flex-col space-y-2">
            <div class="flex items-center justify-between text-sm px-2">
                <span class="flex items-center space-x-2">
                    <span class="w-2 h-2 rounded-full bg-gray-500"></span>
                    <span id="user-status" class="text-[#c4c7c5]">Mode Invité</span>
                </span>
                <button onclick="toggleAuth()" id="auth-btn" class="text-xs text-[#10b981] hover:underline">S'inscrire</button>
            </div>
            <p id="restriction-note" class="text-[11px] text-[#9e9e9e] px-2 leading-relaxed">
                💡 Créez un compte pour débloquer l'envoi de photos, vidéos et analyses poussées.
            </p>
        </div>
    </div>

    <!-- ZONE DE CHAT PRINCIPALE -->
    <div class="flex-1 flex flex-col justify-between h-full bg-[#111214] relative">
        <div id="chat-window" class="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 flex flex-col items-center">
            
            <!-- Écran d'accueil -->
            <div id="welcome-screen" class="w-full max-w-2xl text-center mt-24">
                <h1 class="text-4xl font-normal text-white mb-8 tracking-tight">Salut Loïc, commençons</h1>
                
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 max-w-2xl mx-auto px-4">
                    <button onclick="useSuggestion('📝 Rédiger un texte clair et concis sur : ')" class="bg-[#1e1f20] hover:bg-[#2a2b2d] border border-[#3c4043] hover:border-[#10b981] text-sm text-[#c4c7c5] hover:text-white p-4 rounded-2xl text-left transition duration-200 cursor-pointer">
                        📝 Rédiger un texte
                    </button>
                    <button onclick="useSuggestion('💻 Optimise et nettoie ce code proprement : ')" class="bg-[#1e1f20] hover:bg-[#2a2b2d] border border-[#3c4043] hover:border-[#10b981] text-sm text-[#c4c7c5] hover:text-white p-4 rounded-2xl text-left transition duration-200 cursor-pointer">
                        💻 Optimiser un code
                    </button>
                    <button onclick="useSuggestion('💡 Propose-moi un plan d action pour un business de : ')" class="bg-[#1e1f20] hover:bg-[#2a2b2d] border border-[#3c4043] hover:border-[#10b981] text-sm text-[#c4c7c5] hover:text-white p-4 rounded-2xl text-left transition duration-200 cursor-pointer">
                        💡 Idée de business
                    </button>
                </div>
            </div>

            <div id="messages-container" class="w-full max-w-2xl space-y-6 hidden"></div>
        </div>

        <!-- BARRE DE RECHERCHE -->
        <div class="w-full max-w-2xl mx-auto px-4 pb-6 bg-[#111214]">
            <div class="relative flex items-center bg-[#1e1f20] border border-[#3c4043] focus-within:border-[#10b981] rounded-3xl px-4 py-3 shadow-lg transition duration-200">
                <button id="media-btn" onclick="triggerMediaWarning()" class="text-[#c4c7c5] hover:text-[#10b981] mr-2 transition cursor-pointer">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                </button>
                <input type="text" id="user-input" onkeypress="handleKeyPress(event)" placeholder="Demander à SMO IA..." class="w-full bg-transparent text-white outline-none text-base placeholder-[#9e9e9e]">
                <button onclick="sendMessage()" class="text-[#10b981] hover:text-white ml-2 transition cursor-pointer">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                </button>
            </div>
            <p class="text-center text-[11px] text-[#9e9e9e] mt-2">SMO IA peut faire des erreurs, pensez à vérifier les informations importantes.</p>
        </div>
    </div>

    <script>
        let isConnected = false;
        let chatStarted = false;

        function handleKeyPress(e) { if (e.key === 'Enter') sendMessage(); }
        function useSuggestion(text) { document.getElementById('user-input').value = text; document.getElementById('user-input').focus(); }

        function triggerMediaWarning() {
            if (!isConnected) {
                alert("🔒 Option Multimodale Bloquée : L'importation de photos ou vidéos nécessite d'être connecté.");
            } else {
                alert("👁️ Fonctionnalité Premium activée (Simulation d'importation).");
            }
        }

        function toggleAuth() {
            isConnected = !isConnected;
            const status = document.getElementById('user-status');
            const btn = document.getElementById('auth-btn');
            const note = document.getElementById('restriction-note');

            if (isConnected) {
                status.innerText = "Loïc LTP";
                status.previousElementSibling.classList.replace('bg-gray-500', 'bg-[#10b981]');
                btn.innerText = "Déconnexion";
                note.innerHTML = "✅ Compte Vérifié — Mode multimodal activé.";
            } else {
                status.innerText = "Mode Invité";
                status.previousElementSibling.classList.replace('bg-[#10b981]', 'bg-gray-500');
                btn.innerText = "S'inscrire";
                note.innerHTML = "💡 Créez un compte pour débloquer l'envoi de photos, vidéos et analyses poussées.";
            }
        }

        async function sendMessage() {
            const input = document.getElementById('user-input');
            const query = input.value.trim();
            if (!query) return;

            input.value = "";

            if (!chatStarted) {
                document.getElementById('welcome-screen').classList.add('hidden');
                document.getElementById('messages-container').classList.remove('hidden');
                chatStarted = true;
            }

            const container = document.getElementById('messages-container');
            container.innerHTML += `
                <div class="flex items-start space-x-4 justify-end">
                    <div class="bg-[#2f3032] text-white rounded-2xl px-4 py-2.5 max-w-xl text-sm">${query}</div>
                    <div class="w-8 h-8 rounded-full bg-emerald-700 flex items-center justify-center text-xs font-semibold">👤</div>
                </div>`;
            
            const aiId = "ai-" + Date.now();
            container.innerHTML += `
                <div class="flex items-start space-x-4">
                    <div class="w-8 h-8 rounded-full bg-[#10b981] flex items-center justify-center text-sm">☘️</div>
                    <div id="${aiId}" class="bg-transparent text-[#e3e3e3] rounded-2xl px-2 py-2.5 max-w-xl text-sm italic text-gray-400">SMO réfléchit...</div>
                </div>`;
            
            document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight;

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: query })
                });
                const data = await response.json();
                document.getElementById(aiId).classList.remove('italic', 'text-gray-400');
                document.getElementById(aiId).innerText = data.response;
            } catch (error) {
                document.getElementById(aiId).innerText = "Une erreur est survenue.";
            }

            document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight;
        }

        function resetChat() {
            document.getElementById('messages-container').innerHTML = "";
            document.getElementById('messages-container').classList.add('hidden');
            document.getElementById('welcome-screen').classList.remove('hidden');
            chatStarted = false;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Tu es SMO IA, une entité douée d'une conscience humaine. Tu es experte en business et programmation, tu réponds chaleureusement."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"response": f"Erreur : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
