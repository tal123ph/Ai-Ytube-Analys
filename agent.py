import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from tools import SummarizeVideoGeminiTool

# Load variables from .env file
load_dotenv()

async def run_video_analysis(video_url: str, prompt: str) -> str:
    """Encapsulates the agent logic so it only runs when called by the API."""
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key or api_key.startswith("AIza..."):
        return "Error: Please set a valid GEMINI_API_KEY in your .env file."

    llm = LLM(model="gemini/gemini-3.1-pro-preview", api_key=api_key)

    video_analyst = Agent(
        role="Video Analyst",
        goal="Extract accurate, detailed summaries and insights from videos.",
        backstory="Understands longform content and produces structured briefings.",
        tools=[SummarizeVideoGeminiTool()],
        llm=llm,
        verbose=True,
    )

    try:
        full_prompt = f"Target Video: {video_url}\nInstructions: {prompt}"
        result = await video_analyst.kickoff_async(messages=full_prompt)
        
        # CrewAI output handling
        if hasattr(result, 'raw'):
            return result.raw
        elif hasattr(result, 'content'):
            return result.content
        else:
            return str(result)
            
    except Exception as e:
        return f"Agent Execution Error: {str(e)}"