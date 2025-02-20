from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/extract-audio', methods=['POST'])
def extract_audio():
    video_id = request.json.get('video_id')
    if not video_id:
        return jsonify({'error': 'No video ID provided'}), 400

    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'extractaudio': True,
        'audioformat': 'mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(id)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
            audio_url = info['url']
            return jsonify({'audio_url': audio_url})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
