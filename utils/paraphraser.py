mkdir parafrase-app
cd parafrase-app
mkdir -p api public utils
touch api/paraphrase.py
touch utils/paraphraser.py
touch requirements.txt
touch vercel.json
touch runtime.txt
touch .gitignore
import os
import requests
import time
import logging

# Setup logging
logger = logging.getLogger(__name__)

class Paraphraser:
    def __init__(self):
        # Gunakan token langsung sebagai fallback
        self.api_token = os.getenv("HF_API_TOKEN", "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")
        self.api_url = "https://api-inference.huggingface.co/models/cahya/t5-base-indonesian-paraphrase"
        logger.info("Paraphraser initialized with token: %s", self.api_token[:4] + "****")
    
    def chunk_text(self, text, max_chunk_words=300):
        """Membagi teks besar menjadi bagian-bagian kecil"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_count = 0
        
        for word in words:
            current_chunk.append(word)
            current_count += 1
            if current_count >= max_chunk_words:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_count = 0
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks

    def paraphrase_large_text(self, text):
        """Memparafrase teks besar dengan chunking"""
        if not text.strip():
            return "Teks kosong"
            
        chunks = self.chunk_text(text)
        paraphrased_chunks = []
        
        for i, chunk in enumerate(chunks):
            payload = {"inputs": f"parafrase: {chunk}"}
            headers = {"Authorization": f"Bearer {self.api_token}"}
            
            try:
                logger.info("Processing chunk %d/%d: %s...", i+1, len(chunks), chunk[:20])
                response = requests.post(
                    self.api_url, 
                    headers=headers, 
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
                        generated_text = result[0]['generated_text'].replace("parafrase: ", "")
                        paraphrased_chunks.append(generated_text)
                    else:
                        logger.warning("Unexpected response format: %s", response.text)
                        paraphrased_chunks.append(chunk)
                elif response.status_code == 503:
                    logger.warning("Model loading, waiting 10 seconds...")
                    time.sleep(10)
                    return self.paraphrase_large_text(text)  # Retry
                else:
                    logger.error("API error: %d - %s", response.status_code, response.text)
                    paraphrased_chunks.append(f"[Error {response.status_code}] {chunk}")
            except Exception as e:
                logger.exception("Exception during API call")
                paraphrased_chunks.append(f"[Exception] {str(e)}")
        
        return " ".join(paraphrased_chunks)
