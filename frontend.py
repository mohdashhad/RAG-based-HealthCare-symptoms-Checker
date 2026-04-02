import streamlit as st
import requests

st.set_page_config(page_title="Healthcare Symptom Checker", page_icon="🏥")

st.title("🏥 Healthcare Symptom Checker")
st.write("Enter your symptoms below to get possible conditions and recommendations.")

# Input box
symptoms = st.text_area("Enter symptoms (e.g., fever, headache):")

# Button
if st.button("Check Symptoms"):
    if symptoms.strip() == "":
        st.warning("⚠️ Please enter symptoms")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/check",
                json={"symptoms": symptoms}
            )

            data = response.json()

            # Conditions
            st.subheader("🩺 Possible Conditions")
            for condition in data.get("conditions", []):
                st.write(f"• {condition}")

            # Severity
            st.subheader("⚠️ Severity")
            severity = data.get("severity", "N/A")

            if severity == "high":
                st.error(severity.upper())
            elif severity == "medium":
                st.warning(severity.upper())
            else:
                st.success(severity.upper())

            # Next Steps
            st.subheader("💊 Recommended Steps")
            for step in data.get("next_steps", []):
                st.write(f"• {step}")

            # Disclaimer
            st.subheader("📢 Disclaimer")
            st.info(data.get("disclaimer", ""))

        except Exception as e:
            st.error("❌ Failed to connect to backend")