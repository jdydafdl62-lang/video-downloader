from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api/v1/extract', methods=['POST'])
def extract_video():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {
        'format': 'best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            direct_url = info_dict.get('url', None)
            title = info_dict.get('title', 'video')
            
            return jsonify({
                'success': True,
                'title': title,
                'download_url': direct_url
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
