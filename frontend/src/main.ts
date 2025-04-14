// Get DOM elements
const recordBtn = document.getElementById("record-btn") as HTMLButtonElement;
const stat = document.getElementById("status") as HTMLElement;

// Initialize MediaRecorder and storage for audio chunks
let mediaRecorder: MediaRecorder;
let audioChunks: Blob[] = [];

// Handle record button click
recordBtn.onclick = async () => {
  // If already recording, stop the recording
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    recordBtn.textContent = "Start Recording";
    return;
  }

  // Request microphone access and create MediaRecorder
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  audioChunks = []; // Reset audio chunks array

  // Event handler for new audio data
  mediaRecorder.ondataavailable = (event) => {
    audioChunks.push(event.data);
  };

  // Event handler for when recording stops
  mediaRecorder.onstop = async () => {
    // Create a Blob from the recorded audio chunks
    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
    console.log("Audio Blob type:", audioBlob.type);
    
    // Prepare form data for API request
    const formData = new FormData();
    formData.append("audio", audioBlob, "audio.wav");

    try {
      // Send audio to backend for emotion detection
      const response = await fetch("http://localhost:8000/detect-emotion", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      
      // Handle different response scenarios
      if (data.emotion) {
          stat.textContent = `Detected Emotion: ${data.emotion}`;
      } else if (data.error) {
          stat.textContent = `Server error: ${data.error}`;
      } else {
          stat.textContent = "Unexpected response format.";
      }

    } catch (error) {
      // Handle any errors during the API call
      console.error("Error:", error);
      stat.textContent = "Error detecting emotion.";
    }
  };

  // Start recording
  mediaRecorder.start();
  recordBtn.textContent = "Stop Recording";
  stat.textContent = "Recording...";
};
