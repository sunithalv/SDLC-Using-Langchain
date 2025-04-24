import streamlit as st
from src.sdlc.graph.graph_builder import GraphBuilder
from src.sdlc.LLMS.groqllm import GroqLLM
from src.sdlc.LLMS.openaillm import OpenAILLM
from src.sdlc.ui.uiconfigfile import Config
import base64


def get_cached_graph():
    """Cache the model so it persists across reruns."""
    user_input=st.session_state.get('user_input','')
    if user_input['selected_llm'] == 'Groq':
        obj_llm_config = GroqLLM(user_controls_input=user_input)
    elif user_input['selected_llm'] == 'OpenAI':
        obj_llm_config = OpenAILLM(user_controls_input=user_input)
    else:
        st.error("Invalid LLM selection.")
        return
    model = obj_llm_config.get_llm_model()
    graph_builder = GraphBuilder(model)
    return graph_builder.setup_graph()


@st.cache_data
def get_cached_sdlc_nodes():
    sdlc_nodes = Config().get_sdlc_nodes()
    sdlc_nodes = sdlc_nodes.split(",")
    return sdlc_nodes

def clear_cache_data():
    st.session_state.clear()
    st.cache_data.clear()  # Clear all cached data
    st.cache_resource.clear()  # Clear all cached resources
    st.session_state.page = "home"

def display_states(curr_state,response):
    state=curr_state.replace('_', ' ')
    b64_docs = base64.b64encode(response.encode()).decode()
    href = f'''
        <a href="data:text/markdown;base64,{b64_docs}" 
        download="{curr_state}.md"
        style="text-decoration: none; color: inherit; font-weight: bold;">
            ⬇️ Download {state}
        </a>
    '''
    st.markdown(href, unsafe_allow_html=True)




