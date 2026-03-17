# API cloud code block update, Add API usage log, removed API key, added a Auditor, added a PDF upload

import streamlit as st
from openai import OpenAI
import json
from pypdf import PdfReader
import os
import datetime
from dotenv import load_dotenv

# 1. LOAD SECURITY & CONFIG
load_dotenv()

# --- CLOUD & LOCAL COMPATIBILITY ---
# This looks at Streamlit Secrets FIRST (Cloud), then .env (Local)
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="MBA Job Matcher Pro", page_icon="🚀")
st.title("Tier-1 Job Matcher 🎯")

# --- USAGE TRACKER LOGIC ---
def log_usage():
    log_file = "usage_log.json"
    try:
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                data = json.load(f)
        else:
            data = {"total_runs": 0, "history": []}

        data["total_runs"] += 1
        data["history"].append(str(datetime.datetime.now()))

        with open(log_file, "w") as f:
            json.dump(data, f, indent=4)
        return data["total_runs"]
    except Exception:
        # On some cloud platforms, writing files is restricted. 
        # We catch the error so the app doesn't crash.
        return "N/A"

# --- HELPER FUNCTIONS ---
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# --- SIDEBAR STATS ---
st.sidebar.title("App Dashboard")
if os.path.exists("usage_log.json"):
    try:
        with open("usage_log.json", "r") as f:
            stats = json.load(f)
        st.sidebar.metric("Total Scans Performed", stats["total_runs"])
    except:
        st.sidebar.info("Analytics temporarily unavailable.")
else:
    st.sidebar.info("No scans recorded yet.")

# --- UI INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.write("### 1. Your Resume")
    uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")
    manual_resume = st.text_area("Or Paste/Edit Resume Text here...", height=200)
    
    if uploaded_file is not None:
        resume_content = extract_text_from_pdf(uploaded_file)
        st.success("PDF Content Loaded!")
    else:
        resume_content = manual_resume

with col2:
    st.write("### 2. Job Description")
    jd_content = st.text_area("Paste the Job Description here...", height=325)

# --- AGENT PROMPTS ---
enhancer_system = """
You are a Senior Executive Recruiter for Tier-1 MBA roles. 
Analyze Resume vs JD and provide JSON output:
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

auditor_system = """
ROLE: Forensic Fact-Checker. 
YOUR GOAL: Ensure 100% "Grounding" (Truthfulness) to the Raw Resume.

STRICT RULES:
1. ZERO TOLERANCE FOR NEW CONTEXT: If the original resume mentions "Pipeline" and the draft mentions "City-level business," REJECT it. 
2. NO INVENTING SCOPE: Do not assume the user worked in different sectors, locations, or scales than what is explicitly written.
3. DATA INTEGRITY: If the original doesn't have a specific metric or location, the draft MUST NOT have one.
4. CORRECTION PROTOCOL: If you find a hallucination, your 'final_verified_bullet' must revert the bullet to the original resume's language, but with better formatting.

OUTPUT JSON:
{
  "is_grounded": bool, 
  "hallucination_detected": "string (specifically name what was invented)",
  "audit_notes": "string", 
  "final_verified_bullet": "string"
}
"""

# --- EXECUTION ---
if st.button("Run Match Analysis"):
    if not api_key:
        st.error("API Key missing! If on Cloud, add it to Secrets. If Local, check .env.")
    elif not resume_content or not jd_content:
        st.error("Please provide both a Resume and a JD.")
    else:
        client = OpenAI(api_key=api_key)
        
        try:
            # PASS 1: THE ENHANCER
            with st.spinner("Agent 1: Strategizing Enhancement..."):
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
            with st.spinner("Agent 2: Fact-Checking Draft..."):
                # Safety check for the draft
                draft = res1.get('xyz_upgrade', {}).get('enhanced_draft', 'No draft generated')
                
                response_2 = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                       {"role": "system", "content": auditor_system},
                       {"role": "user", "content": f"RAW_RESUME: {resume_content}\nENHANCED_DRAFT: {draft}"}
                    ],
                    response_format={"type": "json_object"}
                )
                res2 = json.loads(response_2.choices[0].message.content)

            # LOG USAGE
            log_usage()

# --- DISPLAY RESULTS ---
            st.divider()
            
            c1, c2 = st.columns(2)
            with c1:    
                st.metric(label="Match Score", value=f"{res1.get('match_score', 0)}%")
            with c2:
                st.write("**Seniority Alignment:**")
                st.write(res1.get("seniority_alignment", "N/A"))

            st.error(f"**Critical Gap:** {res1.get('critical_missing_skill')}")

            st.write("### 💡 Verified Resume Power-Up")
            
            # --- NEW HALLUCINATION DETECTION UI ---
            if res2.get("is_grounded"):
                st.success("✅ Fact-Check Passed: No hallucinations found.")
            else:
                # If a hallucination is detected, we show the specific detail it caught in RED
                st.error(f"🚨 Hallucination Caught: {res2.get('hallucination_detected')}")
                st.warning(f"⚠️ Auditor Note: {res2.get('audit_notes')}")

            st.code(res2.get("final_verified_bullet"), language="text")
            
            # --- KEEPING YOUR ORIGINAL EXPANDER ---
            with st.expander("Show Audit Comparison"):
                st.write("**Original Resume Point:**", res1.get('xyz_upgrade', {}).get('original'))
                st.write("**AI's Proposed Draft:**", res1.get('xyz_upgrade', {}).get('enhanced_draft'))
                st.info(f"**2026 Market Context:** {res1.get('market_insight')}")

        except Exception as e:
            st.error(f"Workflow Error: {e}")