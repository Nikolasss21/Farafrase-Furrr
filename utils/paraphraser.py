import os
import requests
import time

class Paraphraser:
    def __init__(self):
        self.api_token = os.getenv("HF_API_TOKEN", "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")
        self.api_url = "https://api-inference.huggingface.co/models/cahya/t5-base-indonesian-paraphrase"
    
    def chunk_text(self, text, max_chunk_words=300):
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
        chunks = self.chunk_text(text)
        paraphrased_chunks = []
        
        for chunk in chunks:
            payload = {"inputs": f"parafrase: {chunk}"}
            headers = {"Authorization": f"Bearer {self.api_token}"}
            
            try:
                response = requests.post(
                    self.api_url, 
                    headers=headers, 
                    json=payload,
                    timeout=120  # Timeout 2 menit
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
                        generated_text = result[0]['generated_text'].replace("parafrase: ", "")
                        paraphrased_chunks.append(generated_text)
                    else:
                        paraphrased_chunks.append(chunk)
                elif response.status_code == 503:
                    # Model masih loading, tunggu dan coba lagi
                    time.sleep(15)
                    return self.paraphrase_large_text(text)
                else:
                    paraphrased_chunks.append(f"[Error: {response.status_code}] {chunk}")
            except Exception as e:
                paraphrased_chunks.append(f"[Exception] {str(e)}")
        
        return " ".join(paraphrased_chunks)
