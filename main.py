from utils.variables import GEMINI_API_KEY, ELEVENLABS_API_KEY
from google import genai
from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google.genai import types
from utils.model import system_instruction_text
from elevenlabs.client import ElevenLabs

class Question(BaseModel):
    question:str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"),name="static")

@app.post("/get-response")
def response(item:Question):
    # Creación de la respuesta de Gemini 
    client_genai = genai.Client(api_key=GEMINI_API_KEY)
    text_response = client_genai.models.generate_content(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(system_instruction=system_instruction_text),
            contents=[item.question]
        ).text
    client_elevenlabs = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    audio = client_elevenlabs.text_to_speech.convert(
        text=text_response,
        voice_id="bN1bDXgDIGX5lw0rtY2B",
        output_format="mp3_44100_128"
    )
    audio_name="response.mp3"
    audio_path=f"./static/{audio_name}"
    
    with open (audio_path,"wb") as f:
        for chunk in audio: 
            f.write(chunk)

    
    return {"text":text_response,"audio":f"http://127.0.0.1:8000/static/{audio_name}"}

