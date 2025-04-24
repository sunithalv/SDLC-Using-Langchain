import streamlit as st
from src.sdlc.utils.utils import display_states
import base64
import json

def display_downloads(self):
    state = self.graph.get_state(config=st.session_state.thread)  # Fetch the state from the graph
    state_dict = state.values  
    st.write("### Downloadable assets from the SDLC")
    for key, value in state_dict.items():
        if key=="generated_code":
            # Convert ZIP to base64
            zip_bytes = st.session_state.zip_buffer.getvalue()
            b64_zip = base64.b64encode(zip_bytes).decode()
            # Create a download link
            href = f'''<a href="data:application/zip;base64,{b64_zip}" 
            download="generated_code.zip" 
            style="text-decoration: none; color: inherit; font-weight: bold;">⬇️ Download code files</a>'''
            st.markdown(href, unsafe_allow_html=True) 
        elif key=="qa_testing":
            #Convert the list to a JSON string
            json_str = json.dumps(value['details'])
            display_states(self.curr_state, json_str)
        elif key in self.sdlc_nodes and key !="consolidated_artifacts":
            display_states(key,value)


    