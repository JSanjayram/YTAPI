from flask import Flask, redirect, request, session, url_for, jsonify
from google_auth_oauthlib.flow import Flow
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with a random secret key

# Path to your client secrets file
CLIENT_SECRETS_FILE = 'cs.json'  # Update this path if necessary

# OAuth 2.0 scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

@app.route('/')
def index():
    return 'Welcome! <a href="/authorize">Login with Google</a>'

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='https://ytapi-1-0cq0.onrender.com/oauth2callback'  # Use the Render URI
    )
    authorization_url, state = flow.authorization_url(access_type='offline')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=session['state'],
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    return redirect(url_for('get_audio_uri', video_id='gEC8IEZYxc0'))  # Replace with your video ID

@app.route('/get-audio-uri/<video_id>')
def get_audio_uri(video_id):
    if 'credentials' not in session:
        return redirect('authorize')

    credentials = session['credentials']
    headers = {'Authorization': f'Bearer {credentials["token"]}'}
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=status'
    response = requests.get(url, headers=headers)
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

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
