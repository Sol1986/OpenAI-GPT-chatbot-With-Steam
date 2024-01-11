import streamlit as st #imports streamlit
from openai import OpenAI
client = OpenAI()
import os
from dotenv import load_dotenv, find_dotenv
from streamlit_chat import message

load_dotenv(find_dotenv(), override = True)

os.getenv('OPENAI_API_KEY')


st.set_page_config(
    page_icon='🤖',  # Custom favicon, you can use a URL or an emoji
    layout='wide',   # Choose 'wide' or 'centered' layout
)

with st.sidebar:
  st.image('chatbot.png', width=200)
  api_key = st.text_input('OpenAI API Key:', type='password')
  if api_key:
    os.environ['OPENAI_API_KEY']= api_key


#Creates a title
st.subheader(' Welcome To Your AI Chat Assistant 🤖')
st.text('Ask me anything')

#pick the model we want to use
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

#initialize chat history by setting it to an empty array
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages = [{"role": "system", "content": "A helpful assistant that answers as concisely as possible."}]

#Display chat message from history on app rerun with the message provided by the ruser
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



#get user input and store it in a variable
prompt = st.chat_input("How can I help you?")



#check if the prompt has been provided
if prompt: # means if the prompt is true
    #display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    #add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    #display assistant response in chat message container
    with st.chat_message("assistant"):
        #create a empty place holder which will be filled later
        message_placeholder = st.empty()
        #crate an empty string which will be used to slowly build the chat response
        full_response = ""
        #call the openAI API
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"], # pass model
            messages=[
                
                {"role": m["role"], "content": m["content"]} # pass conversation history used by model
                for m in st.session_state.messages
            ],
            temperature=0.5,
            frequency_penalty= 0.2,
            top_p= 0.5,
            stream=True, #to slowly get the chatgpt reponse
        ):
            # add the response with spaces to the full response empty string variable 
            if response.choices[0].delta.content is not None:
                full_response += response.choices[0].delta.content
            #add the full response to the message placeholder variable that is empty container. Add a | to give it a thinking effect
            print(message_placeholder.markdown(full_response +"| "))
        #add the full response to the message placerholder    
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})


