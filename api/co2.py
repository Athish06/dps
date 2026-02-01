"""
Consolidated CO-2 API
Contains: RSA
This reduces serverless function count for Vercel Hobby plan limit
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import importlib.util

def load_module(name):
    """Dynamically load a module from the api/lib directory"""
    module_path = os.path.join(os.path.dirname(__file__), 'lib', f'{name}.py')
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "CO-2 Cipher API ready",
            "ciphers": ["rsa"]
        }).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            cipher = data.get('cipher', 'rsa')
            result = None
            
            if cipher == 'rsa':
                module = load_module('rsa')
                p = int(data.get('p', 61))
                q = int(data.get('q', 53))
                e = int(data.get('e', 17))
                m = int(data.get('m', 65))
                result = module.rsa_encrypt_detailed(p, q, e, m)
            
            else:
                result = {"success": False, "error": f"Unknown cipher: {cipher}"}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as ex:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(ex)
            }).encode('utf-8'))
