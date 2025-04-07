from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import PlainTextResponse
import uvicorn
import tempfile
import os
from faster_whisper import WhisperModel
import re

app = FastAPI()

# Load Whisper model globally
model = WhisperModel("base", device="cpu", compute_type="int8")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/v1/audio/transcriptions", response_class=PlainTextResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    model_name: str = Form("whisper-1"),  # Renamed parameter to avoid shadowing
    response_format: str = Form("text")
):
    # Check if the file is an audio file
    print("testing")
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file_path = temp_file.name
        contents = await file.read()
        temp_file.write(contents)
    
    try:
        # Transcribe using faster-whisper (now using the global model)
        segments, info = model.transcribe(temp_file_path)
        text = " ".join([segment.text for segment in segments]).strip()
        
        # If client requested text format, return as is
        if response_format == "text":
            return text
        else:
            # Return JSON format if requested
            return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)