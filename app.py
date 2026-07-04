from flask import Flask, render_template, request, send_file, jsonify
from downloader import download_youtube_audio
import os

app = Flask(__name__)

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        file_path, title = download_youtube_audio(url)
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f'{title}.mp3',
            mimetype='audio/mpeg'
        )
        
    except Exception as e:
        return jsonify({'error': 'Download failed. Please try again or use a different video.'}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))