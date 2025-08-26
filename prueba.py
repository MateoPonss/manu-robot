from elevenlabs.client import ElevenLabs
from elevenlabs import play

client = ElevenLabs(api_key="sk_755bc18fb5d985d0d7cf1f00e6a80f742c8efd47e9305f10")

audio = client.text_to_speech.convert(
    text="Hola desde Baradero, me llamo Melanie",
    voice_id="bN1bDXgDIGX5lw0rtY2B",
    output_format="mp3_44100_128"
)

audio_path="respuesta.mp3"
with open (audio_path,"wb") as f:
    for chunk in audio: 
        f.write(chunk)