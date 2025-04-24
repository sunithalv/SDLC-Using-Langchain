import streamlit as st
from src.sdlc.ui.uiconfigfile import Config

#Sidebar with the user controls
class LoadStreamlitUI:
    def __init__(self):
        self.config =  Config() # config
        self.user_controls = {}

    def initialize_session(self):
        return {
        "sdlc": ""
    }


    def load_streamlit_ui(self):
        st.set_page_config(page_title= "🛠️ " + self.config.get_page_title(), layout="wide")     

        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                # API key input
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key",
                                                                                                      type="password")
            elif self.user_controls["selected_llm"] == 'OpenAI':
                # Model selection
                model_options = self.config.get_openai_model_options()
                self.user_controls["selected_openai_model"] = st.selectbox("Select Model", model_options)
                # API key input
                self.user_controls["OPENAI_API_KEY"] = st.session_state["OPENAI_API_KEY"] = st.text_input("API Key",
                                                                                                      type="password")
            
            if "state" not in st.session_state:
                st.session_state.state = self.initialize_session()
            
        return self.user_controls