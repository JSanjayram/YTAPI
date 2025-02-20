from fastapi import FastAPI, HTTPException
import yt_dlp
import random

# Example free proxy list (replace with actual proxies)
PROXY_LIS = [
    "http://219.65.73.81:80",
    "http://202.131.153.146:1111",
    "http://103.137.218.65:83",
    "http://210.16.92.0:58080",
    "http://160.25.180.35:8080",
]
PROXY_LIST = [
    "http://103.139.98.67",
    "http://202.145.10.251",
    "http://8.215.12.103",
    "http://124.158.153.218",
    "http://27.112.66.18",
]

proxy = random.choice(PROXY_LIST)
API_KEY = "AIzaSyAoQwPeQ0beBRsgSdq4e4TAxFpTdrY97Yo"
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the YouTube Audio API!"}

@app.get("/get-audio-uri/{video_id}")
async def get_audio_uri(video_id: str):
    try:
        url =f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet,contentDetails,statistics&key={API_KEY}'
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': False,
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'geo_bypass': True,  # Attempt to bypass geographic restrictions
           # 'proxy': proxy,  # Using the selected proxy
            'socket_timeout': 60  # Increase timeout to 60 seconds

        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            audio_url = [f['url'] for f in formats if f.get('acodec') != 'none'][0]

        return {"audio_uri": audio_url}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting audio URL: {str(e)}")
