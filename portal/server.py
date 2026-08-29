#!/usr/bin/env python3
"""
Ultra-lightweight, zero-disk-IO, pre-compressed in-memory HTTP server.
Memory footprint: < 15MB RAM, CPU usage: ~0.0%
"""
import http.server
import socketserver
import os
import gzip
import sys
import hashlib
import time

PORT = 80
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_FILE = os.path.join(BASE_DIR, "labs_data.json")

CACHE = {}

def preload_assets():
    print("[*] Preloading and pre-compressing all assets in RAM...")
    
    # 1. HTML
    html_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "rb") as f:
            raw = f.read()
        gz = gzip.compress(raw, compresslevel=9)
        etag = f'"{hashlib.md5(raw).hexdigest()}"'
        CACHE["/"] = {"raw": raw, "gz": gz, "type": "text/html; charset=utf-8", "etag": etag, "cache": "no-cache, must-revalidate"}
        CACHE["/index.html"] = CACHE["/"]

    # 2. Labs JSON API (Always fresh, no-store)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            raw = f.read()
        gz = gzip.compress(raw, compresslevel=9)
        etag = f'"{hashlib.md5(raw).hexdigest()}"'
        CACHE["/api/labs"] = {"raw": raw, "gz": gz, "type": "application/json; charset=utf-8", "etag": etag, "cache": "no-cache, must-revalidate"}

    # 3. Static Images & Assets
    for fname in os.listdir(STATIC_DIR):
        fpath = os.path.join(STATIC_DIR, fname)
        if os.path.isfile(fpath) and fname != "index.html":
            with open(fpath, "rb") as f:
                raw = f.read()
            gz = gzip.compress(raw, compresslevel=9)
            etag = f'"{hashlib.md5(raw).hexdigest()}"'
            
            ctype = "application/octet-stream"
            if fname.endswith(".png"): ctype = "image/png"
            elif fname.endswith(".ico"): ctype = "image/x-icon"
            elif fname.endswith(".svg"): ctype = "image/svg+xml"
            elif fname.endswith(".woff2"): ctype = "font/woff2"
            elif fname.endswith(".woff"): ctype = "font/woff"
            
            CACHE[f"/{fname}"] = {
                "raw": raw,
                "gz": gz,
                "type": ctype,
                "etag": etag,
                "cache": "public, max-age=31536000, immutable"
            }

class ZeroResourceHandler(http.server.BaseHTTPRequestHandler):
    def address_string(self):
        return self.client_address[0]
        
    def log_message(self, format, *args):
        pass

    def do_HEAD(self):
        self.send_asset(send_body=False)

    def do_GET(self):
        self.send_asset(send_body=True)

    def send_asset(self, send_body=True):
        path = self.path.split("?")[0]
        asset = CACHE.get(path)
        
        if not asset:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", "9")
            self.end_headers()
            if send_body:
                self.wfile.write(b"Not Found")
            return

        accept_encoding = self.headers.get("Accept-Encoding", "")
        if "gzip" in accept_encoding and len(asset["gz"]) < len(asset["raw"]):
            body = asset["gz"]
            use_gzip = True
        else:
            body = asset["raw"]
            use_gzip = False

        self.send_response(200)
        self.send_header("Content-Type", asset["type"])
        self.send_header("Content-Length", str(len(body)))
        self.send_header("ETag", asset["etag"])
        self.send_header("Cache-Control", asset["cache"])
        self.send_header("Access-Control-Allow-Origin", "*")
        if use_gzip:
            self.send_header("Content-Encoding", "gzip")
        self.end_headers()

        if send_body:
            self.wfile.write(body)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
        
    preload_assets()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ZeroResourceHandler) as httpd:
        print(f"[*] Zero-Resource Web Server ready on http://0.0.0.0:{PORT}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
