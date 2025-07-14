# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from get_response_gemeni import AskGemeni

# Replace this with your actual Gemini model code
def get_answer_from_gemini(question: str) -> str:
    # Dummy answer for example purposes
    return f"Gemini's answer to: {question}"

app = FastAPI()

# Allow frontend to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:5500"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(q: Question):
    answer = AskGemeni(q.question)
    return {"answer": answer}
    
@app.get("/")
def read_index():
    return FileResponse("index.html")  # Ensure this path is correct


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
