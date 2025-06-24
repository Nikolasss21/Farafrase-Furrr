import os
import json
from http import HTTPStatus
from flask import jsonify
from utils.paraphraser import Paraphraser

# Inisialisasi paraphraser (akan di-cache di antara pemanggilan)
paraphraser = None

def load_model():
    global paraphraser
    if paraphraser is None:
        paraphraser = Paraphraser()
        paraphraser.initialize()

def handler(request):
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', HTTPStatus.NO_CONTENT, headers)
    
    # Load model jika belum dimuat
    load_model()
    
    # Dapatkan data dari request
    if request.method == 'POST':
        try:
            content_type = request.headers.get('Content-Type')
            if content_type == 'application/json':
                data = request.get_json()
                text = data.get('text', '')
            else:
                text = request.form.get('text', '')
            
            if not text:
                return jsonify({'error': 'Teks tidak boleh kosong'}), HTTPStatus.BAD_REQUEST
            
            # Proses parafrase
            result = paraphraser.paraphrase_large_text(text)
            
            # Response dengan CORS headers
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
            
            return (json.dumps({'result': result}), HTTPStatus.OK, headers)
        
        except Exception as e:
            return jsonify({
                'error': 'Terjadi kesalahan server',
                'details': str(e)
            }), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        return jsonify({'error': 'Metode tidak diizinkan'}), HTTPStatus.METHOD_NOT_ALLOWED
