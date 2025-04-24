import streamlit as st
import uuid
import base64
from src.sdlc.utils.utils import get_cached_sdlc_nodes, get_cached_graph, display_states
from src.sdlc.ui.streamlitui.display_code import display_code_files
from src.sdlc.ui.streamlitui.display_qa_testing import display_qa_results
from src.sdlc.ui.streamlitui.display_artifacts import display_downloads
from langgraph.types import Command
import json

class DisplayResultStreamlit:
    def __init__(self):  
        if "graph" not in st.session_state or st.session_state.page == "home":
            st.session_state.graph = get_cached_graph()  
        self.graph = st.session_state.graph  # Use cached graph
        if not self.graph:
            st.error("Graph is missing! Restart the SDLC process.")
            return
        self.user_requirements = st.session_state.user_requirements
        self.sdlc_nodes = get_cached_sdlc_nodes()
        if "thread" not in st.session_state:
            st.session_state.thread = {"configurable": {"thread_id": str(uuid.uuid4())}}
        if "curr_state" not in st.session_state:
            st.session_state.curr_state = self.sdlc_nodes[0]  # Start from first stage

        # Initialize breadcrumbs in session state
        if "breadcrumbs" not in st.session_state:
            st.session_state.breadcrumbs = []
        if "feedback_text" not in st.session_state:
            st.session_state.feedback_text = ""

    def generate_sdlc(self):
        try:
            self.index = self.sdlc_nodes.index(st.session_state.curr_state)
            request_payload = None
                
            if self.index == 0:
                request_payload = {"user_requirements": self.user_requirements}

            response = ""

            for event in self.graph.stream(request_payload, config=st.session_state.thread, stream_mode="values"):
                response = event.get(st.session_state.curr_state, "")
                review = event.get("generated_code_review", "")
                if st.session_state.curr_state == "generated_code" and review:
                    self.feedback = review

        except KeyError as e:
            st.error(f"Graph execution error: Missing key {e}")
            response = None
        except Exception as e:
            st.error(f"Graph execution error: {e}")

        return response

    def display_result_on_ui(self):
        self.curr_state = st.session_state.curr_state  # Get current state
        response = self.generate_sdlc()  

        # Update breadcrumbs
        if self.curr_state not in st.session_state.breadcrumbs:
            st.session_state.breadcrumbs.append(self.curr_state)
        
        # Define layout with right-side progress column
        col_main, col_sidebar = st.columns([3, 1])

        with col_sidebar:
            st.markdown("### 🔗 SDLC Progress")

            for idx, state in enumerate(self.sdlc_nodes):
                display_name = state.replace('_', ' ').title()

                if state == self.curr_state:
                    # ✅ Current node: green border, bold, larger font
                    st.markdown(
                        f"""
                        <div style="
                            padding: 6px 12px;
                            margin-bottom: 6px;
                            border-left: 4px solid #2e7d32;
                            color: white;
                            font-size: 15px;
                            font-weight: bold;">
                            🔄 {display_name}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                elif state in st.session_state.breadcrumbs:
                    # ✅ Completed node
                    st.markdown(
                        f"""
                        <div style="
                            padding: 6px 12px;
                            margin-bottom: 6px;
                            color: #ccc;
                            font-size: 14px;">
                            ✅ {display_name}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:
                    # ⏳ Upcoming node
                    st.markdown(
                        f"""
                        <div style="
                            padding: 6px 12px;
                            margin-bottom: 6px;
                            color: #888;
                            font-size: 14px;">
                            ⏳ {display_name}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )




        with col_main:
            # Display the main SDLC phase
            state = self.curr_state.replace('_', ' ')
            st.subheader(f"🛠️ **SDLC Phase: {state.title()}**")
            if self.curr_state=="qa_testing":
                print(response)

            if response:
                #with st.expander(f"📜 **{state}**", expanded=True):
                if self.curr_state == "consolidated_artifacts":
                    display_downloads(self)
                elif self.curr_state == "generated_code":
                    display_code_files(self, response)
                elif self.curr_state == "qa_testing":
                    display_qa_results(self,response)
                else:
                    st.markdown(response)

                if self.curr_state != "consolidated_artifacts" and self.curr_state != "generated_code":
                    with st.form(key="feedback_form", clear_on_submit=True):
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                    approve = st.form_submit_button("✅ Approve")
                            with col2:
                                if self.curr_state != "qa_testing" and self.curr_state != "deployment" and self.curr_state !="maintanence_and_updates":
                                    feedback = st.text_area("Provide feedback if not approved", value=st.session_state.feedback_text, key="feedback_input")
                                    submit_feedback = st.form_submit_button("Submit Feedback")
                            status=""
                            if self.curr_state == "qa_testing" or self.curr_state == "deployment" or self.curr_state =="maintanence_and_updates":
                                submit_feedback=""
                                feedback=""
                                if self.curr_state == "qa_testing":
                                    status=response


                            if approve:
                                try:
                                    self.graph.invoke(Command(resume=status), config=st.session_state.thread)
                                    if self.index < len(self.sdlc_nodes) - 1:
                                        st.session_state.curr_state = self.sdlc_nodes[self.index + 1]
                                        st.session_state.feedback_text = ""
                                        st.rerun()
                                except ValueError:
                                    st.error("No nodes found!")

                            elif submit_feedback and feedback:
                                st.session_state.feedback_text = feedback
                                self.graph.invoke(Command(resume=feedback), config=st.session_state.thread)
                                if self.curr_state =="monitoring_and_feedback" and self.index < len(self.sdlc_nodes) - 1:
                                    st.session_state.curr_state = self.sdlc_nodes[self.index + 1]
                                st.session_state.feedback_text = ""
                                st.rerun()

                    if self.curr_state=="qa_testing":
                        #Convert the list to a JSON string
                        json_str = json.dumps(response['details'])
                        display_states(self.curr_state, json_str)
                    elif self.curr_state != "generated_code":
                        display_states(self.curr_state, response)

                st.session_state.graph = self.graph  
                st.session_state.feedback_text = ""  # Reset feedback            
            else:
                st.error("Error occurred. Please restart the SDLC cycle.")
