from fastapi import FastAPI,Response
from pydantic import BaseModel
from utils import extract_articles, comparative_analysis 
import uvicorn

app = FastAPI()

class CompanyRequest(BaseModel):
    company: str

@app.post("/analyze/")
def analyze_company_news(request: CompanyRequest):
    """Extract news articles and perform complete analysis."""
    articles = extract_articles(request.company) 
    
    if not articles:
        return {"message": f"No articles found for {request.company}"}
    
    analysis_result = comparative_analysis(articles, request.company)
    
    return analysis_result

@app.get("/play-audio/")
def play_audio():
    """Serve an audio file as a response."""
    audio_path = "complete_analysis.mp3"  # Replace with your actual file path
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
    
    return Response(content=audio_data, media_type="audio/mpeg")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
