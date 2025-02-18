import os
from fastapi import FastAPI, HTTPException
import yt_dlp

# Access environment variables
YT_API_KEY = os.getenv("YT_API_KEY")

app = FastAPI()

@app.get("/get-audio-uri/{video_id}")
async def get_audio_uri(video_id: str):
    try:
        # Example of using the environment variable
        if not YT_API_KEY:
            raise HTTPException(status_code=500, detail="API key is missing.")

        url = f'https://www.youtube.com/watch?v={video_id}'

        # Set up yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'extractaudio': True,
            'audioquality': 1,
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredcodec': 'mp3',
            }],
            'noplaylist': True,
            'headers': {
                'Authorization': f'Bearer {YT_API_KEY}'  # Example of using the API key
            },
        }

        # Extract audio URL using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            audio_url = info_dict['formats'][0]['url']

        return {"audio_uri": audio_url}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
