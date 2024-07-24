import openai 
import streamlit as st
import time 

api_key = ""

# Titre de l'application
st.title("GUISSE Chatbot")     

openai.api_key = api_key

# Initialiser l'historique des chats et le modèle OpenAI
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique des chats
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
#------------------------------------------------
# Réagir à la saisie de l'utilisateur
if prompt := st.chat_input("Ask your question"):
    # Afficher le message de l'utilisateur dans l'historique
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Ajouter le message de l'utilisateur à l'historique 
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Réponse au chat de l'assistant
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Création de la réponse en utilisant l'API OpenAI
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[ 
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            time.sleep(0.1)
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "|")
        
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
