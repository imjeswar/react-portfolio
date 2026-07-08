from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from backend.api.deps import get_current_user
from backend.database.models import User
import io

router = APIRouter(prefix="/voice", tags=["Voice Services"])

@router.post("/speech")
async def speech_to_text(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Transcribes an uploaded audio file (speech-to-text placeholder)."""
    # Placeholder return
    return {
        "text": "This is a mock transcription of the uploaded audio file.",
        "confidence": 0.98,
        "language": "en"
    }

@router.post("/tts")
def text_to_speech(
    text: str,
    current_user: User = Depends(get_current_user)
):
    """Synthesizes text into audio stream (text-to-speech placeholder)."""
    # Create a mock 1-second silent WAV file in memory
    mock_audio = io.BytesIO()
    # Write a simple RIFF WAVE header + some silent data
    mock_audio.write(b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x40\x1f\x00\x00\x40\x1f\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00')
    mock_audio.seek(0)
    
    return StreamingResponse(
        mock_audio,
        media_type="audio/wav",
        headers={"Content-Disposition": "attachment; filename=speech.wav"}
    )
