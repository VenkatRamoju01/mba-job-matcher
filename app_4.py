# Removed API key, added a Auditor, added a PDF upload


import streamlit as st
from openai import OpenAI
import json
from pypdf import PdfReader
import os # New import for system paths
from dotenv import load_dotenv # New import to load your vault

# Load the .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="MBA Job Matcher Pro", page_icon="🚀")
st.title("Tier-1 Job Matcher 🎯")

# --- Helper Function for PDF ---
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# --- UI INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.write("### 1. Your Resume")
    uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")
    manual_resume = st.text_area("Or Paste/Edit Resume Text here...", height=200)
    
    if uploaded_file is not None:
        resume_content = extract_text_from_pdf(uploaded_file)
        st.success("PDF uploaded successfully!")
    else:
        resume_content = manual_resume

with col2:
    st.write("### 2. Job Description")
    jd_content = st.text_area("Paste the Job Description here...", height=325)


# --- AGENT 1: THE ENHANCER PROMPT ---
enhancer_system = """
You are a Senior Executive Recruiter for Tier-1 MBA roles. 
Analyze the Resume vs JD and provide a rigorous gap analysis.
Rewrite one specific bullet point using the Google XYZ Formula (Accomplished [X] as measured by [Y], by doing [Z]).

OUTPUT ONLY JSON:
{
  "match_score": integer,
  "seniority_alignment": "string",
  "critical_missing_skill": "string",
  "xyz_upgrade": {
      "original": "string",
      "enhanced_draft": "string",
      "strategy": "string"
  },
  "market_insight": "string"
}
"""

# --- AGENT 2: THE AUDITOR PROMPT ---
auditor_system = """
You are a Forensic Auditor. Compare the ENHANCED_DRAFT bullet point to the RAW_RESUME.
Your goal is to prevent resume fraud.

TRUTH RUBRIC:
1. NO NEW METRICS: If the draft adds a %, $, or # not in the raw text, replace it with '[X]'.
2. NO TITLE INFLATION: Ensure Job Titles and Company names are 100 percent identical to Raw.
3. NO SCOPE CREEP: If 'Assisted' became 'Led' without evidence, revert the verb.

OUTPUT ONLY JSON:
{
  "is_grounded": boolean,
  "audit_notes": "string",
  "final_verified_bullet": "string"
}
"""

if st.button("Run Match Analysis"):
    if not api_key:
        st.error("Please enter your API key in the sidebar!")
    elif not resume_content or not jd_content:
        st.error("Please provide both a Resume and a Job Description.")
    else:
        client = OpenAI(api_key=api_key)
        
        try:
            # PASS 1: THE ENHANCER
            with st.spinner("Agent 1: Analyzing and Enhancing..."):
                response_1 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                       {"role": "system", "content": enhancer_system},
                       {"role": "user", "content": f"RESUME: {resume_content}\nJD: {jd_content}"}
                    ],
                    response_format={"type": "json_object"}
                )
                res1 = json.loads(response_1.choices[0].message.content)

            # PASS 2: THE AUDITOR
            with st.spinner("Agent 2: Auditing for Truth..."):
                response_2 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                       {"role": "system", "content": auditor_system},
                       {"role": "user", "content": f"RAW_RESUME: {resume_content}\nENHANCED_DRAFT: {res1['xyz_upgrade']['enhanced_draft']}"}
                    ],
                    response_format={"type": "json_object"}
                )
                res2 = json.loads(response_2.choices[0].message.content)

            # --- FINAL DISPLAY ---
            st.divider()
            
            # Metrics Row
            c1, c2 = st.columns(2)
            with c1:    
                st.metric(label="Match Score", value=f"{res1.get('match_score', 0)}%")
            with c2:
                st.write("**Seniority Alignment:**")
                st.write(res1.get("seniority_alignment", "N/A"))

            # Insight Row
            st.write(f"**2026 Market Insight:** {res1.get('market_insight')}")
            st.error(f"**Critical Gap:** {res1.get('critical_missing_skill')}")

            # The Auditor's Verified Output
            st.write("### 💡 Verified Resume Power-Up")
            
            if res2.get("is_grounded"):
                st.success("✅ Fact-Check Passed: All metrics verified against original resume.")
            else:
                st.warning(f"⚠️ Fact-Check Note: {res2.get('audit_notes')}")

            st.write("**Final Suggested Bullet (Copy/Paste below):**")
            st.code(res2.get("final_verified_bullet"), language="text")
            
            with st.expander("Show Technical Audit Details"):
                st.write("**Original:**", res1['xyz_upgrade']['original'])
                st.write("**AI's Ambitious Draft:**", res1['xyz_upgrade']['enhanced_draft'])
                st.write("**Strategic Reason:**", res1['xyz_upgrade']['strategy'])

        except Exception as e:
            st.error(f"Analysis Error: {e}")