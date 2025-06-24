from http import HTTPStatus
from flask import jsonify, request
from utils.paraphraser import Paraphraser

paraphraser = Paraphraser()

def handler(req):
    # Handle CORS
    if request.method == 'OPTIONS':
        return jsonify({}), HTTPStatus.NO_CONTENT, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            text = data.get('text', '')
            
            if not text:
                return jsonify({'error': 'Text is required'}), HTTPStatus.BAD_REQUEST
            
            # Process text
            result = paraphraser.paraphrase_large_text(text)
            
            return jsonify({'result': result}), HTTPStatus.OK, {
                'Access-Control-Allow-Origin': '*'
            }
        
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'details': str(e)
            }), HTTPStatus.INTERNAL_SERVER_ERROR, {
                'Access-Control-Allow-Origin': '*'
            }
    
    return jsonify({'error': 'Method not allowed'}), HTTPStatus.METHOD_NOT_ALLOWED, {
        'Access-Control-Allow-Origin': '*'
    }
