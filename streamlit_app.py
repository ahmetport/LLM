# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import openai
import streamlit as st

# Sidebar configuration
with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')
    # Check if the API key is already set in the secrets
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        # Input for API key if not set
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key) == 51):
            st.warning('Please enter a valid API key!', icon='⚠️')
        else:
            st.success('API key is valid. You can now proceed!', icon='👉')

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new messages
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            # Generate responses using OpenAI API
            response = openai.Completion.create(
                model="gpt-4",  # Specify the model name here
                prompt=prompt,
                max_tokens=150
            )
            full_response = response.choices[0].text.strip()
            message_placeholder.markdown(full_response)
        except Exception as e:
            message_placeholder.error(f"Failed to generate response: {e}")

        # Append the response to session state
        st.session_state.messages.append({"role": "assistant", "content": full_response})

