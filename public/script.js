// Hitung kata saat ketik
document.getElementById('inputText').addEventListener('input', function() {
    const text = this.value.trim();
    const wordCount = text ? text.split(/\s+/).length : 0;
    document.getElementById('wordCount').textContent = wordCount;
    
    if (wordCount > 2000) {
        this.style.borderColor = '#e74c3c';
        document.getElementById('paraphraseBtn').disabled = true;
    } else {
        this.style.borderColor = '#3498db';
        document.getElementById('paraphraseBtn').disabled = false;
    }
});

// Fungsi proses parafrase
document.getElementById('paraphraseBtn').addEventListener('click', processParaphrase);

function processParaphrase() {
    const text = document.getElementById('inputText').value.trim();
    const wordCount = text ? text.split(/\s+/).length : 0;
    
    if (!text) {
        showError('Harap masukkan teks terlebih dahulu');
        return;
    }
    
    if (wordCount > 2000) {
        showError('Teks melebihi batas maksimal 2000 kata');
        return;
    }
    
    // Tampilkan loading
    document.getElementById('loadingIndicator').style.display = 'flex';
    document.getElementById('errorContainer').style.display = 'none';
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('resultText').innerHTML = '';
    document.getElementById('copyBtn').style.display = 'none';
    
    // Kirim permintaan ke server
    fetch('/api/paraphrase', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('loadingIndicator').style.display = 'none';
        
        if (data.error) {
            showError(data.error);
        } else {
            document.getElementById('resultText').innerHTML = 
                `<p>${data.result.replace(/\n/g, '<br>')}</p>`;
            document.getElementById('successMessage').style.display = 'block';
            document.getElementById('copyBtn').style.display = 'block';
        }
    })
    .catch(error => {
        document.getElementById('loadingIndicator').style.display = 'none';
        showError('Terjadi kesalahan: ' + error.message);
    });
}

// Fungsi untuk menampilkan error
function showError(message) {
    const errorContainer = document.getElementById('errorContainer');
    errorContainer.textContent = message;
    errorContainer.style.display = 'block';
}

// Fungsi untuk menyalin hasil
document.getElementById('copyBtn').addEventListener('click', function() {
    const resultText = document.getElementById('resultText').textContent;
    navigator.clipboard.writeText(resultText)
        .then(() => {
            alert('Teks berhasil disalin ke clipboard!');
        })
        .catch(err => {
            alert('Gagal menyalin teks: ' + err);
        });
});
