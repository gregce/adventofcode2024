function updateStatus(message, isError, type = 'info') {
    var status = document.getElementById('status');
    var newEntry = document.createElement('div');
    
    // Style based on type
    let className = 'mb-2 ';
    switch(type) {
        case 'success':
            className += 'text-green-400';
            break;
        case 'error':
            className += 'text-red-400';
            break;
        case 'api':
            className += 'text-blue-400';
            break;
        case 'file':
            className += 'text-yellow-400';
            break;
        default:
            className += 'text-green-400';
    }
    
    newEntry.className = className;
    var timestamp = new Date().toLocaleTimeString();
    newEntry.textContent = '[' + timestamp + '] ' + message;
    status.appendChild(newEntry);
    status.scrollTop = status.scrollHeight;
}

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    document.getElementById(tabName + '-tab').style.display = 'block';
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('bg-[#00cc00]', 'text-black');
        button.classList.add('text-[#00cc00]');
    });
    document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('bg-[#00cc00]', 'text-black');
    document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.remove('text-[#00cc00]');
}

function submitForm(event) {
    event.preventDefault();
    var form = event.target;
    var submitBtn = form.querySelector('button[type="submit"]');
    var formData = new FormData(form);
    
    submitBtn.disabled = true;
    document.getElementById('result-container').innerHTML = '';
    updateStatus(' Starting generation process...', false);
    
    const eventSource = new EventSource('/generate/status');
    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        updateStatus(data.message, data.error, data.type);
        
        if (data.spec) {
            updateResultSection('spec', data.spec);
        }
        if (data.solution) {
            updateResultSection('solution', data.solution);
        }
        if (data.result) {
            updateResultSection('result', data.result);
        }
        
        if (data.complete) {
            eventSource.close();
        }
    };
    
    fetch('/generate', {
        method: 'POST',
        body: formData
    })
    .then(function(response) {
        if (!response.ok) {
            return response.text().then(function(text) {
                throw new Error(text || 'Server error');
            });
        }
        return response.text();
    })
    .then(function(result) {
        document.getElementById('result-container').innerHTML = result;
        updateStatus('✨ Generation completed successfully!', false, 'success');
        eventSource.close();
    })
    .catch(function(error) {
        console.error('Error:', error);
        updateStatus('❌ ' + error.message, true, 'error');
        eventSource.close();
    })
    .finally(function() {
        submitBtn.disabled = false;
    });
}

function updateResultSection(type, content) {
    const tab = document.getElementById(`${type}-tab`);
    if (tab) {
        const pre = tab.querySelector('pre');
        if (pre) {
            pre.textContent = content;
        }
        showTab(type);
    }
}

function showTab(type) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    document.getElementById(`${type}-tab`).style.display = 'block';
    
    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('bg-[#00cc00]', 'text-black');
        button.classList.add('text-[#00cc00]');
    });
    const activeButton = document.querySelector(`[onclick="switchTab('${type}')"]`);
    if (activeButton) {
        activeButton.classList.add('bg-[#00cc00]', 'text-black');
        activeButton.classList.remove('text-[#00cc00]');
    }
}

function downloadText(content, filename, type) {
    // Create the blob with proper MIME type
    const mimeTypes = {
        'text/python': 'text/plain',  // Python files are plain text
        'text/markdown': 'text/markdown',
        'text/plain': 'text/plain'
    };

    try {
        const blob = new Blob([content], { 
            type: mimeTypes[type] || 'text/plain'
        });

        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;

        // Add to document, click, and cleanup
        document.body.appendChild(a);
        a.click();
        
        // Small timeout to ensure download starts
        setTimeout(() => {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 100);
    } catch (error) {
        console.error('Download error:', error);
        console.log('Content:', content);
    }
}

function resetApp() {
    // Clear status log
    document.getElementById('status').innerHTML = '';
    
    // Clear result container
    document.getElementById('result-container').innerHTML = '';
    
    // Reset form
    document.querySelector('form').reset();
    
    // Add initial status message
    updateStatus('App reset successfully', false, 'success');
}

async function submitApiKey(event) {
    event.preventDefault();
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const formData = new FormData(form);
    
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/set-api-key', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to set API key');
        }
        
        // Reload page on success
        window.location.reload();
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error setting API key: ' + error.message);
    } finally {
        submitBtn.disabled = false;
    }
} 