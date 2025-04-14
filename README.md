# Voice Emotion Detection Chatbot

This project is a full-stack chatbot that detects a user's emotional tone from their voice using a pretrained Hugging Face model and returns a contextual response. The frontend records audio and sends it to a FastAPI backend which runs an emotion classification model.

## Features

- Real-time voice recording in the browser
- Pretrained emotion detection using wav2vec2
- FastAPI backend with Torch + Hugging Face
- Five supported emotion classes: angry, happy, sad, neutral, surprised
- TypeScript frontend

## Tech Stack

- Frontend: HTML, TypeScript
- Backend: FastAPI, PyTorch, Hugging Face Transformers
- Audio Processing: torchaudio, pydub, ffmpeg

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/shaheersajid07/Moody-Chatbot.git
cd Moody-Chatbot
```

### 2. Backend Setup (FastAPI)

```bash
cd backend
```

Install required Python packages:

```bash
pip install fastapi uvicorn transformers torchaudio pydub soundfile
```

Install ffmpeg and add it to your system PATH:

1. Download the Windows build from https://www.gyan.dev/ffmpeg/builds/
2. Extract the archive and copy the path to the bin directory (e.g., `C:\ffmpeg\bin`)
3. Add that path to your system’s Environment Variables → System → Path
4. Restart your terminal and verify it works:

```bash
ffmpeg -version
```

Run the backend server:

```bash
uvicorn index:app --reload --port 8000
```

### 3. Frontend Setup (TypeScript)

```bash
cd ../frontend
```

```bash
npm install
```

In the frontend dir, use `npm run dev -- --port=3000` to run on `http://localhost:3000`


Make sure the backend is running on port 8000 before starting the frontend.

## Usage

- Press "Start Recording" to capture a 3-second voice clip.
- The audio is sent to the backend for processing.
- The backend returns a predicted emotion based on vocal tone.
- The result is displayed in the interface, for example:

```
Detected Emotion: happy
```

## Supported Emotions

- angry  
- happy  
- sad  
- neutral  
- surprised  

## Future Enhancements

- Increased accuracy
- Custom chatbot replies based on detected mood
- Save user emotion history to a database
- Visual feedback with confidence scores
