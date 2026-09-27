from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from agent import run_video_analysis
from audio_utils import text_to_audio_file, remove_temp_file

app = FastAPI(title="Video Summarizer API")
STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")

@app.get("/")
async def root():
    return {
        "message": "Video Summarizer API is running",
        "docs": "/docs",
        "endpoints": ["POST /summarize", "POST /summarize-audio"],
    }

class VideoRequest(BaseModel):
    video_url: str
    prompt: str = "Summarize this video and provide a list of action items."

@app.post("/summarize")
async def summarize_video(request: VideoRequest):
    try:
        summary = await run_video_analysis(request.video_url, request.prompt)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize-audio")
async def summarize_video_to_audio(request: VideoRequest, background_tasks: BackgroundTasks):
    try:
        summary_text = await run_video_analysis(request.video_url, request.prompt)
        
        if "Error:" in summary_text or "Gemini error:" in summary_text:
             raise HTTPException(status_code=400, detail=summary_text)

        audio_file_path = text_to_audio_file(summary_text)
        background_tasks.add_task(remove_temp_file, audio_file_path)
        
        return FileResponse(
            path=audio_file_path, 
            media_type="audio/mpeg", 
            filename="video_summary.mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))