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

# Optional: auto-open browser
try:
    import webbrowser
    import threading
    def open_browser():
        webbrowser.open(f'http://localhost:{PORT}')
    threading.Timer(1.0, open_browser).start()
except:
    pass

with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
