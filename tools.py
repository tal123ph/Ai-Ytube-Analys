import os
from typing import Optional
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

def _summarize_video_with_genai(
    video_url: str,
    prompt: str,
    model: str,
    stream: bool,
    mime_type: str,
    response_mime_type: str,
) -> str:
    """Internal helper that calls the Google AI Studio SDK."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Missing GEMINI_API_KEY. Please set it first in your .env file."

    client = genai.Client(api_key=api_key)

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(
                    file_data=types.FileData(
                        file_uri=video_url,
                        mime_type=mime_type,
                    )
                ),
                types.Part.from_text(text=prompt),
            ],
        )
    ]
    cfg = types.GenerateContentConfig(response_mime_type=response_mime_type)

    try:
        if stream:
            chunks = []
            for chunk in client.models.generate_content_stream(
                model=model, contents=contents, config=cfg
            ):
                if getattr(chunk, "text", None):
                    chunks.append(chunk.text)
            return ("".join(chunks)).strip() or "No text returned."
        else:
            resp = client.models.generate_content(
                model=model, contents=contents, config=cfg
            )
            return (getattr(resp, "text", "") or "").strip() or "No text returned."
    except Exception as e:
        return f"Gemini error: {e}"

class VideoSummaryArgs(BaseModel):
    video_url: str = Field(description="YouTube or direct video URL")
    prompt: Optional[str] = Field(
        default="Generate a detailed summary with key points and timestamps (if available).",
        description="Instruction for how to summarize"
    )
    stream: Optional[bool] = Field(default=False, description="If True, uses server-side streaming")
    model: Optional[str] = Field(default="gemini-3.1-pro-preview", description="Gemini model name")
    mime_type: Optional[str] = Field(default="video/*", description="Video MIME type")
    response_mime_type: Optional[str] = Field(default="text/plain", description="Response format")

class SummarizeVideoGeminiTool(BaseTool):
    name: str = "summarize_video_gemini"
    description: str = """
    Summarize a video using Gemini (Google AI Studio).

    Args:
        video_url: A YouTube or direct video URL.
        prompt:    Instruction for how to summarize.
        stream:    If True, uses server-side streaming.
        model:     Gemini model name, e.g. 'gemini-3.1-pro-preview'.
        mime_type: Usually 'video/*'.
        response_mime_type: 'text/plain' only (not 'text/markdown').

    Returns:
        Plain text summary.
    """
    args_schema: type[BaseModel] = VideoSummaryArgs

    def _run(
        self,
        video_url: str,
        prompt: str = "Generate a detailed summary with key points and timestamps (if available).",
        stream: bool = False,
        model: str = "gemini-3.1-pro-preview",
        mime_type: str = "video/*",
        response_mime_type: str = "text/plain",
    ) -> str:
        return _summarize_video_with_genai(
            video_url=video_url,
            prompt=prompt,
            model=model,
            stream=stream,
            mime_type=mime_type,
            response_mime_type=response_mime_type,
        )