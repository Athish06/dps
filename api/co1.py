"""
Consolidated CO-1 API
Combines: Monoalphabetic, Hill, ADFGVX, Playfair, SDES, Vigenere
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
            "status": "CO-1 Cipher API ready",
            "ciphers": ["monoalphabetic", "hill", "adfgvx", "playfair", "sdes", "vigenere"]
        }).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            cipher = data.get('cipher', 'monoalphabetic')
            result = None
            
            if cipher == 'monoalphabetic':
                module = load_module('monoalphabetic')
                plaintext = data.get('plaintext', 'HELLO')
                mode = data.get('mode', 'encrypt')
                key_k = data.get('key_k', 3)
                key_a = data.get('key_a', 5)
                key_b = data.get('key_b', 8)
                operation = data.get('operation', 'additive')
                result = module.monoalphabetic_cipher_detailed(plaintext, mode, key_k=key_k, key_a=key_a, key_b=key_b, operation=operation)
            
            elif cipher == 'hill':
                module = load_module('hill')
                plaintext = data.get('plaintext', 'HELLO')
                keyMatrix = data.get('keyMatrix', [[6, 24, 1], [13, 16, 10], [20, 17, 15]])
                m = data.get('m', 3)
                vectorMode = data.get('vectorMode', 'column')
                result = module.hill_cipher_detailed(plaintext, keyMatrix, m, vectorMode)
            
            elif cipher == 'adfgvx':
                module = load_module('adfgvx')
                mode = data.get('mode', 'encrypt')
                poly_key = data.get('polyKey', 'privacy')
                trans_key = data.get('transKey', 'cipher')
                if mode == 'encrypt':
                    plaintext = data.get('plaintext', 'attackat1200am')
                    result = module.encrypt_adfgvx_detailed(plaintext, poly_key, trans_key)
                else:
                    ciphertext = data.get('ciphertext', '')
                    result = module.decrypt_adfgvx_detailed(ciphertext, poly_key, trans_key)
            
            elif cipher == 'playfair':
                module = load_module('playfair')
                plaintext = data.get('plaintext', 'HELLO')
                keyword = data.get('keyword', 'MONARCHY')
                result = module.playfair_cipher_detailed(plaintext, keyword)
            
            elif cipher == 'sdes':
                module = load_module('sdes')
                plaintext = data.get('plaintext', '10111101')
                key = data.get('key', '1010000010')
                P10 = data.get('P10', [3,5,2,7,4,10,1,9,8,6])
                P8 = data.get('P8', [6,3,7,4,8,5,10,9])
                IP = data.get('IP', [2,6,3,1,4,8,5,7])
                EP = data.get('EP', [4,1,2,3,2,3,4,1])
                P4 = data.get('P4', [2,4,3,1])
                S0 = data.get('S0', [["01","00","11","10"],["11","10","01","00"],["00","10","01","11"],["11","01","11","10"]])
                S1 = data.get('S1', [["00","01","10","11"],["10","00","01","11"],["11","00","01","00"],["10","01","00","11"]])
                IP_INV = module.calculate_ip_inverse(IP)
                result = module.encrypt_with_detailed_steps(plaintext, key, P10, P8, IP, IP_INV, EP, P4, S0, S1)
            
            elif cipher == 'vigenere':
                module = load_module('vigenere')
                mode = data.get('mode', 'encrypt')
                cipher_type = data.get('cipherType', 'vigenere')
                key = data.get('key', 'KEY')
                if cipher_type == 'vigenere':
                    if mode == 'encrypt':
                        plaintext = data.get('plaintext', 'HELLO')
                        result = module.vigenere_encrypt_detailed(plaintext, key)
                    else:
                        ciphertext = data.get('ciphertext', '')
                        result = module.vigenere_decrypt_detailed(ciphertext, key)
                else:  # autokey
                    if mode == 'encrypt':
                        plaintext = data.get('plaintext', 'HELLO')
                        result = module.autokey_encrypt_detailed(plaintext, key)
                    else:
                        ciphertext = data.get('ciphertext', '')
                        result = module.autokey_decrypt_detailed(ciphertext, key)
            
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
