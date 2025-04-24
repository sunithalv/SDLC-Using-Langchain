import streamlit as st
from langgraph.types import Command
import zipfile
import io

def create_zip(generated_code):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path, code_content in generated_code.items():
            zip_file.writestr(file_path, code_content)
    zip_buffer.seek(0)
    return zip_buffer

def display_code_files(self, generated_code):
    st.title("Generated Code Review")

    st.subheader("📄 Generated Code Files")

    # Display all code files
    for file_path, code_content in generated_code.items():
        st.markdown(f"**`{file_path}`**")
        st.code(code_content, language="python")  # adjust language as needed

    # Create ZIP only once
    if "zip_buffer" not in st.session_state:
        st.session_state.zip_buffer = create_zip(generated_code)

    # Download button
    st.download_button(
        label="⬇️ Download All as ZIP",
        data=st.session_state.zip_buffer,
        file_name="generated_code.zip",
        mime="application/zip"
    )

    # Inline Approve + Feedback Form
    st.divider()

    with st.form(key="approve_feedback_form"):
        col1, col2 = st.columns([1, 4])  # Adjust ratio as needed

        with col1:
            approve = st.form_submit_button("✅ Approve")

        with col2:
            feedback = st.text_area("Edit/Submit feedback if not approved:", value=self.feedback, height=700)
            submit_feedback = st.form_submit_button("✏️ Submit Feedback")

    if approve:
        self.graph.invoke(Command(resume=""), config=st.session_state.thread)
        if self.index < len(self.sdlc_nodes) - 1:
            st.session_state.curr_state = self.sdlc_nodes[self.index + 1]
            st.session_state.feedback_text = ""
            st.rerun()

    elif submit_feedback and feedback.strip():
        st.session_state.feedback_text = feedback
        self.graph.invoke(Command(resume=feedback), config=st.session_state.thread)
        st.session_state.feedback_text = ""
        st.rerun()
