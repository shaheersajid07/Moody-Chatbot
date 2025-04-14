# Import required libraries
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor
import torch
import torchaudio
from io import BytesIO
from pydub import AudioSegment

# Initialize FastAPI application
app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing)
# This allows the frontend (running on port 3000) to make requests to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the pre-trained emotion recognition model and its components
model_name = "superb/wav2vec2-base-superb-er"
model = AutoModelForAudioClassification.from_pretrained(model_name)
extractor = AutoFeatureExtractor.from_pretrained(model_name)
labels = model.config.id2label  # Dictionary mapping indices to emotion labels (e.g., {0: 'angry', ...})

@app.post("/detect-emotion")
async def detect_emotion(audio: UploadFile = File(...)):
    """
    Endpoint to detect emotion from uploaded audio file
    
    Args:
        audio (UploadFile): The audio file uploaded from the frontend
    
    Returns:
        dict: Contains either the detected emotion or an error message
    """
    try:
        # Read the raw audio data from the uploaded file
        audio_bytes = await audio.read()

        # Convert the audio to a format we can work with
        # Using pydub to handle different input formats and convert to WAV
        audio_segment = AudioSegment.from_file(BytesIO(audio_bytes))
        wav_io = BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)  # Reset buffer position to start

        # Load the audio file using torchaudio
        waveform, sample_rate = torchaudio.load(wav_io)

        # Preprocess the audio to match model requirements
        # Convert to 16kHz sample rate if needed
        if sample_rate != 16000:
            waveform = torchaudio.transforms.Resample(
                orig_freq=sample_rate, 
                new_freq=16000
            )(waveform)
        
        # Convert stereo to mono if needed by averaging channels
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        # Extract features from the audio using the model's feature extractor
        inputs = extractor(
            waveform.squeeze().numpy(), 
            sampling_rate=16000, 
            return_tensors="pt"
        )

        # Make prediction using the model
        with torch.no_grad():  # Disable gradient calculation for inference
            logits = model(**inputs).logits
            predicted_idx = torch.argmax(logits, dim=-1).item()
            emotion = labels[predicted_idx]

        # Return the detected emotion
        return {"emotion": emotion}

    except Exception as e:
        # Log any errors and return error message to frontend
        print("Internal error:", e)
        return {"error": str(e)}
