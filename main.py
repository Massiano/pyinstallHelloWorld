import http.server
import socketserver
import os
import sys
import json

# Find config.json next to the executable (or script)
if getattr(sys, 'frozen', False):
    # Running as PyInstaller bundle
    exe_dir = os.path.dirname(sys.executable)
else:
    # Running as script
    exe_dir = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(exe_dir, 'config.json')

if not os.path.exists(config_path):
    print(f"❌ Missing config.json next to the executable!")
    print(f"Please create: {config_path}")
    input("Press Enter to exit...")
    sys.exit(1)

with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

serve_dir = config.get('serve_dir')
if not serve_dir:
    print("❌ config.json must contain 'serve_dir'")
    sys.exit(1)

# Resolve relative path from config file location
serve_dir = os.path.abspath(os.path.join(exe_dir, serve_dir))

if not os.path.isdir(serve_dir):
    print(f"❌ Folder not found: {serve_dir}")
    sys.exit(1)

PORT = 8000
os.chdir(serve_dir)

print(f"📁 Serving folder: {serve_dir}")
print(f"🔗 Open: http://localhost:{PORT}")

# 👇👇👇 CUSTOM HANDLER WITH SECURITY HEADERS 👇👇👇
class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable cross-origin isolation for SharedArrayBuffer
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        # Optional: allow local dev CORS if needed
        # self.send_header('Cross-Origin-Resource-Policy', 'same-origin')
        super().end_headers()
# 👆👆👆 END CUSTOM HANDLER 👆👆👆

# Optional: auto-open browser
try:
    import webbrowser
    import threading
    def open_browser():
        webbrowser.open(f'http://localhost:{PORT}')
    threading.Timer(1.0, open_browser).start()
except:
    pass

# Use the custom handler
with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
