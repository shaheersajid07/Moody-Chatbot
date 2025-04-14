const recordBtn = document.getElementById("record-btn") as HTMLButtonElement;
const stat = document.getElementById("status") as HTMLElement;

let mediaRecorder: MediaRecorder;
let audioChunks: Blob[] = [];

recordBtn.onclick = async () => {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    recordBtn.textContent = "Start Recording";
    return;
  }

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  audioChunks = [];

  mediaRecorder.ondataavailable = (event) => {
    audioChunks.push(event.data);
  };

  mediaRecorder.onstop = async () => {
    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
    console.log("Audio Blob type:", audioBlob.type);
    const formData = new FormData();
    formData.append("audio", audioBlob, "audio.wav");

    try {
      const response = await fetch("http://localhost:8000/detect-emotion", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
    if (data.emotion) {
        stat.textContent = `Detected Emotion: ${data.emotion}`;
    } else if (data.error) {
        stat.textContent = `Server error: ${data.error}`;
    } else {
        stat.textContent = "Unexpected response format.";
    }

      stat.textContent = `Detected Emotion: ${data.emotion}`;
    } catch (error) {
      console.error("Error:", error);
      stat.textContent = "Error detecting emotion.";
    }
  };

  mediaRecorder.start();
  recordBtn.textContent = "Stop Recording";
  stat.textContent = "Recording...";
};
