
from flask import Flask
import psutil
import os
import time

app = Flask(__name__)

def format_bytes(bytes_value):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024

@app.route('/')
def dashboard():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    load = os.getloadavg()
    uptime = time.time() - psutil.boot_time()
    net = psutil.net_io_counters()

    return f'''
    <html>
    <head>
        <title>ZEETECH Monitoring Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body {{
                font-family: 'Poppins', sans-serif;
                background: url("/static/zeetech-bg.png") no-repeat center top fixed;
                background-size: cover;
                background-position-y: 120px;
                color: #264653;
                text-align: center;
                margin: 0;
                padding: 0;
            }}
            .container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                padding: 20px;
                margin-top: 140px;
            }}
            .card {{
                background: rgba(255, 255, 255, 0.85);
                border-radius: 12px;
                padding: 20px;
                width: 250px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            .card i {{
                font-size: 24px;
                margin-bottom: 10px;
                color: #2a9d8f;
            }}
            footer {{
                margin: 30px auto;
                font-size: 12px;
                color: #ccc;
            }}
            .dark {{
                background-color: #121212 !important;
                color: #eee !important;
            }}
        </style>
    </head>
    <body>
        <button onclick="document.body.classList.toggle('dark')">Toggle Dark Mode</button>
        <div class="container">
            <div class="card">
                <i class="fas fa-microchip"></i>
                <p><strong>CPU Usage:</strong><br>{cpu}%</p>
            </div>
            <div class="card">
                <i class="fas fa-memory"></i>
                <p><strong>Memory Usage:</strong><br>{memory.percent}% of {format_bytes(memory.total)}</p>
            </div>
            <div class="card">
                <i class="fas fa-hdd"></i>
                <p><strong>Disk Usage:</strong><br>{disk.percent}% of {format_bytes(disk.total)}</p>
            </div>
            <div class="card">
                <i class="fas fa-tachometer-alt"></i>
                <p><strong>System Load:</strong><br>{load[0]}, {load[1]}, {load[2]}</p>
            </div>
            <div class="card">
                <i class="fas fa-clock"></i>
                <p><strong>Uptime:</strong><br>{uptime // 3600:.0f}h {(uptime % 3600) // 60:.0f}m</p>
            </div>
            <div class="card">
                <i class="fas fa-network-wired"></i>
                <p><strong>Network:</strong><br>Sent: {format_bytes(net.bytes_sent)}<br>Recv: {format_bytes(net.bytes_recv)}</p>
            </div>
        </div>
        <footer>
            &copy; 2024 ZEETECH Monitoring Dashboard. All rights reserved.
        </footer>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
