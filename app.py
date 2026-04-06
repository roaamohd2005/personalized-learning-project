import streamlit as st
import json
import pandas as pd
from algorithm import generate_personalized_plan

st.set_page_config(page_title="Personalized Learning Plan", layout="wide")
st.title("🎓 Personalized Learning Algorithm")
st.markdown("**Internship Project** – Analyzes student responses and creates a custom study plan")

# Sidebar for uploading data
st.sidebar.header("Upload Student Data")
uploaded_file = st.sidebar.file_uploader("Upload responses (JSON)", type=["json"])

if uploaded_file:
    responses = json.load(uploaded_file)
    plan = generate_personalized_plan(responses)
    
    st.success("✅ Learning Plan Generated Successfully!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Student Overview")
        st.write("**Weak Topics:**", ", ".join(plan["weak_topics"]) if plan["weak_topics"] else "None")
    
    with col2:
        st.subheader("Recommended Study Order")
    
    # Display the plan nicely
    df = pd.DataFrame(plan["recommended_plan"])
    st.dataframe(df, use_container_width=True)
    
    st.download_button("Download Plan as JSON", 
                       data=json.dumps(plan, indent=2),
                       file_name="personalized_learning_plan.json")

else:
    st.info("👆 Upload a JSON file with student responses to generate the plan.")
    st.markdown("**Sample data format:**")
    st.code('''[
  {"topic": "Algebra", "correct": true, "time_sec": 45, "confidence": 8},
  {"topic": "Algebra", "correct": false, "time_sec": 70, "confidence": 4}
]''', language="json")