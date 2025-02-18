from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/get-audio-uri/{video_id}")
async def get_audio_uri(video_id: str):
    try:
        # Construct the YouTube video URL
        url = f'https://www.youtube.com/watch?v={video_id}'
        
        # Set up yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',  # Choose the best audio format
            'quiet': True,  # No console output
            'extractaudio': True,  # Extract audio only
            'audioquality': 1,  # Best quality
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Save file template
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredcodec': 'mp3',  # Or 'aac', 'opus', etc.
            }],
            'noplaylist': True,  # Don't extract from playlists
        }

        # Extract audio URL using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)  # Only fetch info, not the file
            audio_url = info_dict['formats'][0]['url']  # Get the best audio URL

        return {"audio_uri": audio_url}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
