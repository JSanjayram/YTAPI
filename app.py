from flask import Flask, jsonify
import yt_dlp
import requests

app = Flask(__name__)

API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key

@app.get("/get-audio-uri/<video_id>")
def get_audio_uri(video_id):
    # Check if the video is public using YouTube Data API
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={API_KEY}&part=status'
    response = requests.get(url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        video_status = data['items'][0]['status']
        if video_status['privacyStatus'] == 'public':
            # Proceed to extract audio using yt-dlp
            ydl_opts = {
                'format': 'bestaudio',
                'quiet': True,
                'extractaudio': True,
                'audioformat': 'mp3',
                'outtmpl': '%(id)s.%(ext)s',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
                    audio_url = info['url']
                    return jsonify({'audio_url': audio_url})
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Video is not public.'}), 403
    else:
        return jsonify({'error': 'Video not found.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
