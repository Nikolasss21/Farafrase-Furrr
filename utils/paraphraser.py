from transformers import pipeline, AutoTokenizer
import threading

class Paraphraser:
    def __init__(self):
        self.model_loaded = False
        self.tokenizer = None
        self.paraphraser = None
        self.processing_lock = threading.Lock()
    
    def initialize(self, model_name="cahya/t5-base-indonesian-paraphrase"):
        """Muat model hanya sekali saat inisialisasi"""
        if not self.model_loaded:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.paraphraser = pipeline(
                'text2text-generation', 
                model=model_name,
                device=-1  # Gunakan CPU (Vercel tidak support GPU)
            )
            self.model_loaded = True
    
    def chunk_text(self, text, max_chunk_size=300):
        """Membagi teks besar menjadi bagian-bagian kecil"""
        if not self.tokenizer:
            self.initialize()
        
        tokens = self.tokenizer.tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for token in tokens:
            current_chunk.append(token)
            current_length += 1
            
            if current_length >= max_chunk_size:
                chunks.append(self.tokenizer.convert_tokens_to_string(current_chunk))
                current_chunk = []
                current_length = 0
        
        if current_chunk:
            chunks.append(self.tokenizer.convert_tokens_to_string(current_chunk))
        
        return chunks
    
    def paraphrase_large_text(self, text):
        """Memparafrase teks besar dengan chunking"""
        chunks = self.chunk_text(text)
        paraphrased_chunks = []
        
        for chunk in chunks:
            with self.processing_lock:
                result = self.paraphraser(
                    f"parafrase: {chunk}",
                    max_length=512,
                    num_beams=5,
                    num_return_sequences=1
                )[0]['generated_text']
                paraphrased_chunks.append(result.replace("parafrase: ", ""))
        
        return " ".join(paraphrased_chunks)
