document.getElementById('startScan').addEventListener('click', async () => {
    const ip = document.getElementById('targetIp').value;
    const resultsDiv = document.getElementById('scan-results');
    const progressArea = document.getElementById('progress-area');
    const progressFill = document.getElementById('progress-fill');
    
    if (!ip) return alert("Please enter an IP address");

    // Reset UI
    resultsDiv.innerHTML = `[+] Initiating scan on ${ip}...\n`;
    progressArea.style.display = 'block';
    progressFill.style.width = '0%';
    
    // Hamare ports ki list (Top 15)
    const ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389, 8080];
    
    for (let i = 0; i < ports.length; i++) {
        const port = ports[i];
        const percent = ((i + 1) / ports.length) * 100;
        
        // Update Status
        document.getElementById('scan-status').innerText = `Checking Port ${port}...`;
        progressFill.style.width = `${percent}%`;

        try {
            const response = await fetch('/scan_port', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ip: ip, port: port })
            });
            const data = await response.json();

            
            if (data.status === "open") {
                resultsDiv.innerHTML += `<br>[+] <span class="open-port">CRITICAL: Port ${port} (${data.service}) is OPEN</span>\n`;
            } else {
                resultsDiv.innerHTML += `<br><span class="closed-port">[-] Port ${port} is closed</span>\n`;
            }
        } catch (e) {
            resultsDiv.innerHTML += `<br><span class="error-text">[-] Error scanning port ${port}</span>\n`;
        }
        
        // Auto-scroll console to bottom
        resultsDiv.scrollTop = resultsDiv.scrollHeight;
    }
    
    document.getElementById('scan-status').innerText = "Scan Complete.";
});