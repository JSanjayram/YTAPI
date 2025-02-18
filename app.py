from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the YouTube Audio API!"}

@app.get("/get-audio-uri/{video_id}")
async def get_audio_uri(video_id: str):
    try:
        invidious_url = f'https://yewtu.be/api/v1/videos/{video_id}'
        response = requests.get(invidious_url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch video info")

        video_info = response.json()
        audio_formats = [format for format in video_info['adaptiveFormats'] if format['type'].startswith('audio')]
        if not audio_formats:
            raise HTTPException(status_code=404, detail="No audio formats found")

        audio_url = audio_formats[0]['url']
        return {"audio_uri": audio_url}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting audio URL: {str(e)}")
