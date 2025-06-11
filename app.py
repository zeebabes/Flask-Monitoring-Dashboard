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
            <style>
                body {{
                    font-family: Arial;
                    background: #fefefe;
                    text-align: center;
                    margin-top: 50px;
                }}
                h1 {{
                    color: #2a9d8f;
                }}
                p {{
                    font-size: 18px;
                    color: #264653;
                }}
            </style>
        </head>
        <body>
            <img src="/static/Zeetech.png" alt="ZEETECH Logo" width="100"><br>
            <h1>ZEETECH Monitoring Dashboard</h1>
            <p><strong>CPU Usage:</strong> {cpu}%</p>
            <p><strong>Memory Usage:</strong> {memory.percent}% of {format_bytes(memory.total)}</p>
            <p><strong>Disk Usage:</strong> {disk.percent}% of {format_bytes(disk.total)}</p>
            <p><strong>System Load (1/5/15 min):</strong> {load[0]}, {load[1]}, {load[2]}</p>
            <p><strong>Uptime:</strong> {uptime // 3600:.0f}h {(uptime % 3600) // 60:.0f}m</p>
            <p><strong>Network Sent:</strong> {format_bytes(net.bytes_sent)} | <strong>Received:</strong> {format_bytes(net.bytes_recv)}</p>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
