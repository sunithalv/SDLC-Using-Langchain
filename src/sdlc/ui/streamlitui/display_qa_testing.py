import streamlit as st
import pandas as pd

def display_qa_results(self,response):

    # Display summary
    st.subheader("🧪 Test Summary")
    st.write(response['summary'])

    # Display the table in markdown
    st.subheader("📋 Test Table")
    st.markdown(response['table'], unsafe_allow_html=True)

    # Optionally show detailed error info (if any)
    st.subheader("⚠️ Detailed Errors")
    errors = [item for item in response['details'] if item.get("Status") == "❌ Fail"]
    if errors:
        df_errors = pd.DataFrame(errors)
        st.dataframe(df_errors)
    else:
        st.success("No errors found!")