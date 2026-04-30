#!/usr/bin/env python3
"""Simple HTTP server for Ad Machine dashboard."""
import http.server
import os
import webbrowser

PORT = 3456
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"\n  ⚡ Ad Machine Dashboard")
print(f"  → http://localhost:{PORT}\n")

webbrowser.open(f"http://localhost:{PORT}")
http.server.HTTPServer(("", PORT), http.server.SimpleHTTPRequestHandler).serve_forever()
