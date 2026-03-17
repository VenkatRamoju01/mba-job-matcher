# PDF Resume input and text JD input

import streamlit as st
from openai import OpenAI
import json
from pypdf import PdfReader

st.set_page_config(page_title="MBA Job Matcher", page_icon="🚀")
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
    
    # Text area as a fallback or for manual edits
    manual_resume = st.text_area("Or Paste/Edit Resume Text here...", height=200)
    
    # Logic: Prioritize PDF if uploaded
    if uploaded_file is not None:
        resume_content = extract_text_from_pdf(uploaded_file)
        st.success("PDF uploaded successfully!")
    else:
        resume_content = manual_resume

with col2:
    st.write("### 2. Job Description")
    jd_content = st.text_area("Paste the Job Description here...", height=325)

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# --- THE EXPERT PROMPT ---
system_message = """
You are a Senior Executive Recruiter specializing in Tier-1 MBA placements. 
Perform a 'Gap Analysis' that is 10x more rigorous than a standard LLM summary.

STRICT INSTRUCTIONS:
1. SEMANTIC MATCH: Match 'Scope of Responsibility' (e.g., P&L ownership vs budget management).
2. THE 'MISSING' 5%: Identify the one specific technical or domain skill that will get this resume filtered out by an ATS.
3. QUANTITATIVE UPGRADE: Find a 'weak' bullet point in the resume and rewrite it using the 'Google XYZ Formula'.
4. MARKET INSIGHT: Provide a 1-sentence trend for this role in 2026.

OUTPUT ONLY JSON:
{
  "match_score": integer,
  "seniority_alignment": "string",
  "critical_missing_skill": "string",
  "xyz_formula_upgrade": {
      "original": "string",
      "upgraded": "string",
      "reason": "string"
  },
  "market_insight": "string"
}
"""

if st.button("Run Match Analysis"):
    if not api_key:
        st.error("Please enter your API key in the sidebar!")
    elif not resume_content or not jd_content:
        st.error("Please provide both a Resume and a Job Description.")
    else:
        client = OpenAI(api_key=api_key)
        with st.spinner("Analyzing profile against market standards..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                       {"role": "system", "content": system_message},
                       {"role": "user", "content": f"RESUME: {resume_content}\nJD: {jd_content}"}
                    ],
                    response_format={"type": "json_object"}
                )
                
                result = json.loads(response.choices[0].message.content)
                
                # --- DISPLAY ---
                st.divider()
                
                c1, c2 = st.columns(2)
                with c1:    
                    st.metric(label="Match Score", value=f"{result.get('match_score', 0)}%")
                with c2:
                    st.write("**Seniority Alignment:**")
                    st.write(result.get("seniority_alignment", "N/A"))

                st.write("### 🚩 The 'Missing' 5%")
                st.error(result.get("critical_missing_skill", "No critical gaps found."))

                st.write("### 💡 Resume Power-Up (Google XYZ Formula)")
                upgrade = result.get("xyz_formula_upgrade", {})
                st.info(f"**Original:** {upgrade.get('original')}")
                st.success(f"**Upgraded:** {upgrade.get('upgraded')}")
                st.caption(f"*Why this works:* {upgrade.get('reason')}")

                st.info(f"**2026 Insight:** {result.get('market_insight')}")

            except Exception as e:
                st.error(f"Analysis Error: {e}")