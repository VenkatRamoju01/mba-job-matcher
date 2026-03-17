from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# This is a 'Schema' - it tells the Tower exactly what to expect
class ResumeData(BaseModel):
    text: str

@app.post("/analyze")
def analyze(item: ResumeData):
    # Imagine our AI logic lives here
    word_count = len(item.text.split())
    return {
        "message": "Resume received!",
        "word_count": word_count,
        "advice": "This is a good start, but let's add metrics."
    }