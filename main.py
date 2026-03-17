import os
import json
import datetime
import sqlite3 # New: for our database
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# 1. INITIALIZE & SECURITY
load_dotenv()
app = FastAPI(title="MBA Job Matcher API")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- DATABASE LOGIC ---
def init_db():
    """Initializes the SQLite database and creates the table if it doesn't exist."""
    conn = sqlite3.connect("matcher.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            resume_text TEXT,
            jd_text TEXT,
            match_score INTEGER,
            final_bullet TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(resume, jd, score, bullet):
    """Saves a single analysis record to the database."""
    try:
        conn = sqlite3.connect("matcher.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO scans (timestamp, resume_text, jd_text, match_score, final_bullet)
            VALUES (?, ?, ?, ?, ?)
        """, (str(datetime.datetime.now()), resume, jd, score, bullet))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")

# Initialize the database immediately on script load
init_db()

# 2. THE DATA MODELS
class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str

# --- USAGE TRACKER LOGIC (JSON VERSION) ---
def log_usage():
    log_file = "usage_log.json"
    data = {"total_runs": 0, "history": []}
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                data = json.load(f)
        except:
            pass 
    
    data["total_runs"] += 1
    data["history"].append(str(datetime.datetime.now()))
    
    with open(log_file, "w") as f:
        json.dump(data, f, indent=4)
    return data["total_runs"]

# --- AGENT PROMPTS ---
ENHANCER_SYSTEM = """
You are a Senior Executive Recruiter for Tier-1 MBA roles. 
Analyze the Resume vs JD. You MUST return a JSON object with this exact structure:
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

AUDITOR_SYSTEM = """
You are a Forensic Auditor. Compare the ENHANCED_DRAFT to the RAW_RESUME.
Return this exact JSON:
{
  "is_grounded": boolean,
  "audit_notes": "string",
  "final_verified_bullet": "string"
}
"""

# 3. THE ENDPOINT
@app.post("/analyze")
async def run_analysis(request: MatchRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="API Key missing on server.")

    try:
        # PASS 1: THE ENHANCER
        res1_raw = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": ENHANCER_SYSTEM},
                {"role": "user", "content": f"RESUME: {request.resume_text}\nJD: {request.jd_text}"}
            ],
            response_format={"type": "json_object"}
        )
        res1 = json.loads(res1_raw.choices[0].message.content)

        # SAFETY DEFAULTS
        xyz_data = res1.get("xyz_upgrade", {})
        draft_bullet = xyz_data.get("enhanced_draft", "Could not generate draft.")

        # PASS 2: THE AUDITOR
        res2_raw = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": AUDITOR_SYSTEM},
                {"role": "user", "content": f"RAW_RESUME: {request.resume_text}\nENHANCED_DRAFT: {draft_bullet}"}
            ],
            response_format={"type": "json_object"}
        )
        res2 = json.loads(res2_raw.choices[0].message.content)

        # --- NEW: SAVE TO SQLITE DATABASE ---
        save_to_db(
            request.resume_text, 
            request.jd_text, 
            res1.get("match_score", 0), 
            res2.get("final_verified_bullet", "N/A")
        )

        # Log usage to JSON as well
        total_count = log_usage()

        return {
            "status": "success",
            "total_app_usage": total_count,
            "analysis": res1,
            "audit": res2
        }

    except Exception as e:
        print(f"Error caught: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 4. HEALTH CHECK
@app.get("/")
def health_check():
    return {"status": "active", "message": "The MBA Job Matcher Brain is Online"}