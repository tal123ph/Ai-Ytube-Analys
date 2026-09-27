# 🎬 AI Video Analyst

Transform any video into actionable insights — instantly generate text summaries, key points, and audio briefings from YouTube videos using AI.

![AI Video Analyst Home](./screenshots/homepage.png)

---

## 📌 Overview

**AI Video Analyst** is a web application that takes a video URL and turns it into a useful summary — one you can either read as text or listen to as audio. A user enters a video link, the request is routed through an AI agent, and the agent returns a concise explanation, key points, and action items.

### Goals

- ⏱️ Reduce the time required to understand long videos
- 📝 Convert video content into plain-language summaries
- 🔊 Offer an audio version for users who prefer listening while commuting or multitasking

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | **FastAPI** (Python) |
| AI Orchestration | **CrewAI** |
| AI Model | **Google Gemini 3.5 Flash** |
| Text-to-Speech | **gTTS** (Google Text-to-Speech) |
| Frontend | Static HTML/CSS/JavaScript (single-page UI) |
| Config | `python-dotenv` (environment variable management) |
| Server | `uvicorn` |

---

## ✨ Features

### 1. Text Summary Generation
Submit a video URL and an optional custom prompt — the AI agent analyzes the content and returns:
- A general overview of the video
- Main ideas or themes
- Bullet points
- Action items
- Practical takeaways

### 2. Audio Summary Generation
Once a text summary is generated, it's converted to speech via **gTTS** and returned as an MP3 — ideal for listening on the go.

The audio feature generates speech from the summary text; it does not extract or transcribe the video's original audio.

---

## 📸 Screenshots

**Home Page**

![Home Page](./screenshots/homepage.png)

**Text Summary Generator**

![Text Summary Page](./screenshots/text-summary.png)

---

## 🏗️ Project Architecture

```
├── main.py            # FastAPI app & API endpoints
├── agent.py            # AI orchestration layer (CrewAI + Gemini)
├── tools.py            # Custom tool for calling the Gemini API
├── audio_utils.py       # Text-to-speech (gTTS) conversion utilities
└── static/
    └── index.html      # Frontend single-page UI
```

### `main.py`
Defines the FastAPI application and exposes the HTTP endpoints:
- `GET /` — health message and API overview
- `POST /summarize` — receives a video URL and prompt, returns the AI-generated summary
- `POST /summarize-audio` — generates a text summary and converts it to MP3

### `agent.py`
The AI orchestration layer:
- Reads the Gemini API key from environment variables
- Creates a CrewAI LLM instance
- Creates a Video Analyst agent
- Executes the agent with a prompt and video URL
- Handles the result from the AI response

### `tools.py`
Defines the tool used by the AI agent to call Gemini:
- Helper function for sending content to Gemini
- Request-argument schema using Pydantic
- Custom tool class: `SummarizeVideoGeminiTool`

### `audio_utils.py`
Handles audio conversion:
- Creates a temporary MP3 using gTTS
- Deletes temporary files after use

### `static/index.html`
The frontend UI with:
- Home view
- Text Summary tab
- Audio Summary tab
- JavaScript that calls the FastAPI endpoints
- Result display area, audio player, and download button

---

## 🔄 How It Works (End-to-End)

1. User opens the web app.
2. User enters a video URL (and optionally a custom prompt).
3. The browser sends a `POST` request to `/summarize` or `/summarize-audio`.
4. FastAPI receives the request.
5. The request is passed to `run_video_analysis` in `agent.py`.
6. The AI agent creates a Gemini client and asks the model to summarize the content.
7. The result is returned as text.
8. If the audio endpoint is called, the text is forwarded to gTTS and converted into an MP3.
9. The browser plays or downloads the generated audio.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- A valid **Google Gemini API key**

### Installation

```bash
# Clone the repository
git clone https://github.com/tal123ph/<repo-name>.git
cd <repo-name>

# Install dependencies
pip install fastapi uvicorn crewai google-genai gtts python-dotenv pydantic
```

### Environment Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### Run the App

```bash
uvicorn main:app --reload
```

Open the frontend at `http://localhost:8000/static/index.html`. Keep the server running while using the page. The API status is available at `http://localhost:8000/`, and interactive API documentation is at `http://localhost:8000/docs`.

### Use Text and Audio Summaries

1. In the frontend, open **Text Summary** or **Audio Summary**.
2. Enter a YouTube video URL and the instructions for the summary.
3. Submit the form. For an audio summary, wait for the MP3 to be generated, then play it in the page or download it.

The CrewAI agent and direct Gemini video tool currently use `gemini-3.5-flash`. Audio is generated with gTTS and requires an internet connection.

---

## ⚠️ Known Limitations

This project is a **prototype / learning project** and is not yet production-ready. Notable areas for improvement:

- Direct YouTube URL analysis via Gemini may be unreliable without a proper download/extraction pipeline
- Hardcoded model names may become outdated or unsupported
- Limited input validation and error handling
- No automated test suite
- No structured logging or monitoring
- Not yet hardened for public deployment (no auth, rate limiting, HTTPS, or queue-based processing)

---

## 🗺️ Roadmap

- [ ] Add `requirements.txt` / `pyproject.toml`
- [ ] Add a robust video/audio extraction pipeline
- [ ] Validate video URL inputs before calling the AI
- [ ] Add unit and integration tests
- [ ] Add structured logging and error tracking
- [ ] Make the Gemini model name configurable
- [ ] Add retry logic for failed AI calls
- [ ] Add queue-based processing for long-running requests
- [ ] Improve frontend error handling and user feedback

---

## 👤 Author

**Muhammad Talha**

- GitHub: [@tal123ph](https://github.com/tal123ph)
- LinkedIn: [muhammad-talha12b](https://www.linkedin.com/in/muhammad-talha12b)
- Email: *your-email@example.com*

---

## 📄 License

This project is open source and available for learning and personal use.