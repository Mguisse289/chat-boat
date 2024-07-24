import openai
import time
import streamlit as st

# Configuration de l'API OpenAI
api_key = ""
assistant_id = ""
openai.api_key = api_key

# Mettre le titre de la page
st.title("Chatbot assistant Yelloh Village")

# Ajouter les messages à la session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Vérifier si on est sur le même thread
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Afficher les messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Fonction pour créer le thread si nécessaire
def creer_thread_si_besoin():
    if not st.session_state.thread_id:
        client = openai.OpenAI(api_key=api_key)
        chat = client.beta.threads.create(messages=st.session_state.messages)
        st.session_state.thread_id = chat.id

# Réagir à la saisie utilisateur
if prompt := st.chat_input("Posez votre question"):
    with st.chat_message("user"):
        st.markdown(prompt)
    # Ajouter le message de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Créer le thread si nécessaire
    creer_thread_si_besoin()

    # Initialiser le client OpenAI
    client = openai.OpenAI(api_key=api_key)

    # Ajouter le message utilisateur au thread existant
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt
    )

    # Créer un run avec l'ID d'assistant
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )

    # Attendre la complétion du run
    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id
        )

    # Récupérer les messages du thread
    messages_response = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
    messages = messages_response.data
    latest_message = messages[0]  # Récupérer le dernier message

    # Afficher la réponse de l'assistant
    response_text = ""
    for content_item in latest_message.content:
        if content_item.type == 'text':
            response_text += content_item.text.value + " "

    with st.chat_message("assistant"):
        st.markdown(response_text.strip())

    # Ajouter la réponse de l'assistant à l'historique des messages
    st.session_state.messages.append({"role": "assistant", "content": response_text.strip()})
