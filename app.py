from flask import Flask, request, send_file
from datetime import datetime
import csv, io, os

app = Flask(__name__)

LOG_FILE = "tracking_log.csv"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "ip", "user_agent", "email_id"])

@app.route("/track")
def track():
    email_id = request.args.get("id", "unknown")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "unknown")
    ts = datetime.utcnow().isoformat()

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([ts, ip, ua, email_id])

    # 1x1 transparent PNG
    pixel = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdac\xf8\x0f\x00\x01\x01\x01\x00\x18\xdd\x8d\xf7\x00\x00\x00\x00IEND\xaeB`\x82'
    return send_file(io.BytesIO(pixel), mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
