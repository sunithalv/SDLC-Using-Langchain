import streamlit as st
from src.sdlc.ui.streamlitui.loadui import LoadStreamlitUI
from src.sdlc.LLMS.groqllm import GroqLLM
from src.sdlc.LLMS.openaillm import OpenAILLM
from src.sdlc.ui.streamlitui.display_result import DisplayResultStreamlit
from src.sdlc.ui.uiconfigfile import Config
from src.sdlc.utils.utils import clear_cache_data
from src.sdlc import logger


def load_sdlc_app():
    # Check if session state page exists
    if "page" not in st.session_state:
        st.session_state.page = "home"  # Default page
    if st.session_state.page == "home": 
      # Load UI
      ui = LoadStreamlitUI()
      user_input = ui.load_streamlit_ui()

      # Title
      st.title("🛠️ " + Config().get_page_title()) 
      logger.info("In home page")

      with st.form("sdlc_form"):          
        # User Input for Requirements
        user_requirements = st.text_area("📌 Enter your project requirements:")
        if st.form_submit_button("🚀 Start SDLC Cycle") :
            try:
                clear_cache_data() #Clear data from previous cycle
                if user_requirements:
                    user_requirements = user_requirements.strip()
                else:
                    st.error("Please enter your project requirements.")
                    return
                # Initialize LLM
                st.session_state.selected_llm=user_input['selected_llm']
                if user_input['selected_llm'] == 'Groq':
                    if not user_input['GROQ_API_KEY']:
                        st.error("Please enter your Groq API key.")
                        return
                    obj_llm_config = GroqLLM(user_controls_input=user_input)
                elif user_input['selected_llm'] == 'OpenAI':
                    if not user_input['OPENAI_API_KEY']:
                        st.error("Please enter your OPEN AI API key.")
                        return
                    obj_llm_config = OpenAILLM(user_controls_input=user_input)
                else:
                    st.error("Invalid LLM selection.")
                    return

                model = obj_llm_config.get_llm_model()
                if not model:
                    st.error("Error: LLM model could not be initialized.")
                    return

                # Store values in session state
                st.session_state.sdlc_started = True
                st.session_state.user_input = user_input
                st.session_state.user_requirements = user_requirements  # Store input

                # Switch to the result page
                st.session_state.page = "sdlc_result"
                logger.info("Submitted user requirements: %s", user_requirements)
                st.rerun()  # Re-run app to navigate

            except Exception as e:
                st.error(f"Error: {e}")
        
    elif st.session_state.page == "sdlc_result": 
        # Add a button to go back
        if st.button("🔙 Restart SDLC Cycle"):
                clear_cache_data()
                st.rerun() 
        
        with st.spinner("Processing SDLC Results..."):         
            # Call the DisplayResultStreamlit class
            logger.info("Inside state page : ")
            DisplayResultStreamlit().display_result_on_ui()
        




            
            



