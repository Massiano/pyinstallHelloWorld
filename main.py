# server.py
import http.server
import socketserver
import os

PORT = 8000
web_dir = os.path.join(os.path.dirname(__file__), 'web')
os.chdir(web_dir)  # Serve files from ./web folder

with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
