"""
Consolidated Math Operations API
Combines: GCD, Extended Euclidean, Modular Exponentiation, Euler's Theorem, Fermat's Little Theorem
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
            "status": "Math Operations API ready",
            "operations": ["gcd", "extended-euclidean", "mod-exp", "euler", "fermat"]
        }).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            operation = data.get('operation', 'gcd')
            result = None
            
            if operation == 'gcd':
                gcd_module = load_module('gcd')
                a = int(data.get('a', 48))
                b = int(data.get('b', 18))
                result = gcd_module.gcd_detailed(a, b)
            
            elif operation == 'extended-euclidean':
                ee_module = load_module('extended-euclidean')
                a = int(data.get('a', 17))
                m = int(data.get('m', 26))
                result = ee_module.extended_euclidean_detailed(a, m)
            
            elif operation == 'mod-exp':
                me_module = load_module('mod-exp')
                a = int(data.get('a', 7))
                n = int(data.get('n', 256))
                m = int(data.get('m', 13))
                result = me_module.mod_exp_detailed(a, n, m)
            
            elif operation == 'euler':
                euler_module = load_module('euler')
                base = int(data.get('base', 7))
                exponent = int(data.get('exponent', 256))
                modulus = int(data.get('modulus', 13))
                result = euler_module.euler_theorem_detailed(base, exponent, modulus)
            
            elif operation == 'fermat':
                fermat_module = load_module('fermat')
                base = int(data.get('base', 3))
                exponent = int(data.get('exponent', 100))
                modulus = int(data.get('modulus', 7))
                result = fermat_module.fermat_theorem_detailed(base, exponent, modulus)
            
            else:
                result = {"success": False, "error": f"Unknown operation: {operation}"}
            
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
