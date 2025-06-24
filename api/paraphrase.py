mkdir parafrase-app
cd parafrase-app
mkdir -p api public utils
touch api/paraphrase.py
touch utils/paraphraser.py
touch requirements.txt
touch vercel.json
touch runtime.txt
touch .gitignore
from flask import Flask, request, jsonify
from utils.paraphraser import Paraphraser
import os

app = Flask(__name__)

# Inisialisasi paraphraser
paraphraser = Paraphraser()

@app.route('/api/paraphrase', methods=['POST', 'OPTIONS'])
def paraphrase_handler():
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return jsonify({}), 204, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    
    if request.method == 'POST':
        try:
            # Ambil data JSON
            data = request.get_json()
            text = data.get('text', '')
            
            if not text or not text.strip():
                return jsonify({
                    'error': 'Teks tidak boleh kosong',
                    'details': 'Silakan masukkan teks yang ingin diparafrase'
                }), 400
            
            # Proses parafrase
            result = paraphraser.paraphrase_large_text(text)
            
            return jsonify({'result': result}), 200, {
                'Access-Control-Allow-Origin': '*'
            }
        
        except Exception as e:
            return jsonify({
                'error': 'Terjadi kesalahan server',
                'details': str(e)
            }), 500, {
                'Access-Control-Allow-Origin': '*'
            }
    
    return jsonify({'error': 'Metode tidak diizinkan'}), 405, {
        'Access-Control-Allow-Origin': '*'
    }

# Wrapper untuk Vercel
def app_handler(request):
    with app.app_context():
        return paraphrase_handler()
