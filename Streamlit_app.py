import streamlit as st
import openai

st.set_page_config(page_title="Chatbot powered by GPT-3.5 Turbo", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chatbot powered by GPT-3.5 Turbo")

# Sidebar for entering OpenAI key
with st.sidebar:
    st.title('Enter OpenAI API key here:')
    if 'openai_key' in st.secrets:
        st.success('OpenAI key already provided!', icon='✅')
        openai_key = st.secrets['openai_key']
    else:
        openai_key = st.text_input('Enter OpenAI API key here:', type='password', label_visibility="collapsed")
        if not openai_key:
            st.warning('Please enter your OpenAI key!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

# Store chat messages, and initialize the chat message history
if 'messages' not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "I am your AI assistant. Ask me something!"}]

# Display the prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"].replace("$","\$"))

# User-provided prompt
if prompt := st.chat_input(disabled=not openai_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt.replace("$","\$"))

openai.api_key = openai_key

# Function to get the GPT3.5's response
def get_assistant_response(messages):
    r = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
    )
    response = r.choices[0].message.content
    return response

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_assistant_response(st.session_state.messages)
            st.write(response.replace("$","\$"))
    # Add response to message history        
    st.session_state.messages.append({"role": "assistant", "content": response}) 