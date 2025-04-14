from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor
import torch
import torchaudio
from io import BytesIO
from pydub import AudioSegment

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pretrained model
model_name = "superb/wav2vec2-base-superb-er"
model = AutoModelForAudioClassification.from_pretrained(model_name)
extractor = AutoFeatureExtractor.from_pretrained(model_name)
labels = model.config.id2label  # Dictionary: {0: 'angry', ...}

@app.post("/detect-emotion")
async def detect_emotion(audio: UploadFile = File(...)):
    try:
        # Read audio blob from frontend
        audio_bytes = await audio.read()

        # Decode with pydub to ensure correct format
        audio_segment = AudioSegment.from_file(BytesIO(audio_bytes))
        wav_io = BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        # Load audio using torchaudio
        waveform, sample_rate = torchaudio.load(wav_io)

        # Resample to 16kHz mono if needed
        if sample_rate != 16000:
            waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(waveform)
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        # Extract features and predict
        inputs = extractor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits
            predicted_idx = torch.argmax(logits, dim=-1).item()
            emotion = labels[predicted_idx]

        return {"emotion": emotion}

    except Exception as e:
        print("Internal error:", e)
        return {"error": str(e)}
