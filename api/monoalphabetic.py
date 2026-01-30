from http.server import BaseHTTPRequestHandler
import json
import math

def gcd(a, b):
    """Greatest Common Divisor"""
    while b:
        a, b = b, a % b
    return a

def brute_force_inverse_detailed(a, m):
    """Find modular inverse using brute force (trial method)"""
    lines = []
    lines.append(f"Finding inverse of {a} mod {m} using Brute Force Method")
    lines.append("")
    lines.append(f"We need to find x such that: {a} × x ≡ 1 (mod {m})")
    lines.append("")
    lines.append("⚠ Note: This method has HIGH computational cost (O(m) iterations)")
    lines.append("         For large modulus, this becomes very slow!")
    lines.append("")
    lines.append("Trying x = 1, 2, 3, ... until we find ({a} × x) mod {m} = 1")
    lines.append("")
    
    for x in range(1, m):
        product = a * x
        remainder = product % m
        if remainder == 1:
            lines.append(f"  x = {x}: {a} × {x} = {product}, {product} mod {m} = {remainder} ✓ FOUND!")
            lines.append("")
            lines.append(f"★ Inverse of {a} mod {m} = {x}")
            return x, '\n'.join(lines)
        else:
            lines.append(f"  x = {x}: {a} × {x} = {product}, {product} mod {m} = {remainder}")
    
    lines.append("")
    lines.append(f"✗ No inverse found! {a} and {m} are not coprime.")
    return None, '\n'.join(lines)

def extended_euclidean_detailed(a, m):
    """Extended Euclidean Algorithm with detailed table"""
    lines = []
    lines.append(f"Finding inverse of {a} mod {m} using Extended Euclidean Algorithm")
    lines.append("")
    lines.append("This method is EFFICIENT (O(log m) iterations)")
    lines.append("")
    lines.append("Theory:")
    lines.append(f"  We want to find d such that: {a} × d ≡ 1 (mod {m})")
    lines.append(f"  Using Extended Euclidean: {a} × d + {m} × k = gcd({a}, {m})")
    lines.append(f"  If gcd = 1, then d mod {m} is our inverse")
    lines.append("")
    
    # Initialize table
    r1, r2 = m, a
    t1, t2 = 0, 1
    
    lines.append("Extended Euclidean Algorithm Table:")
    lines.append("=" * 60)
    lines.append(f"{'Step':<6} {'Q':<6} {'r1':<8} {'r2':<8} {'r':<8} {'t1':<8} {'t2':<8} {'t':<8}")
    lines.append("-" * 60)
    lines.append(f"{'Init':<6} {'-':<6} {r1:<8} {r2:<8} {'-':<8} {t1:<8} {t2:<8} {'-':<8}")
    
    step = 1
    while r2 > 0:
        q = r1 // r2
        r = r1 % r2
        t = t1 - (q * t2)
        
        lines.append(f"{step:<6} {q:<6} {r1:<8} {r2:<8} {r:<8} {t1:<8} {t2:<8} {t:<8}")
        
        r1, r2 = r2, r
        t1, t2 = t2, t
        step += 1
    
    lines.append("=" * 60)
    lines.append("")
    
    # Explain the table columns
    lines.append("Column Explanations:")
    lines.append("  Q = r1 ÷ r2 (integer division)")
    lines.append("  r = r1 - Q × r2 (remainder)")
    lines.append("  t = t1 - Q × t2 (back-substitution coefficient)")
    lines.append("")
    
    if r1 != 1:
        lines.append(f"Result: gcd({a}, {m}) = {r1}")
        lines.append(f"✗ Since gcd ≠ 1, no inverse exists!")
        lines.append(f"  {a} and {m} are NOT coprime.")
        return None, '\n'.join(lines)
    
    lines.append(f"Result: gcd({a}, {m}) = {r1} ✓")
    lines.append("")
    
    # Adjust if negative
    if t1 < 0:
        lines.append(f"The coefficient t1 = {t1} is negative")
        lines.append(f"Adjusting: {t1} + {m} = {t1 + m}")
        t1 = t1 + m
    
    lines.append("")
    lines.append(f"★ Inverse of {a} mod {m} = {t1}")
    lines.append("")
    lines.append(f"Verification: {a} × {t1} = {a * t1}")
    lines.append(f"              {a * t1} mod {m} = {(a * t1) % m} ✓")
    
    return t1, '\n'.join(lines)

def monoalphabetic_cipher_detailed(plaintext, mode, key_k=None, key_a=None, key_b=None, operation='encrypt'):
    """Monoalphabetic cipher with detailed steps for all modes"""
    all_sections = []
    
    # Section 1: Input Parameters
    input_lines = []
    input_lines.append(f"Plaintext: \"{plaintext}\"")
    input_lines.append(f"Mode: {mode.upper()}")
    input_lines.append(f"Operation: {operation.upper()}")
    input_lines.append("")
    
    if mode == 'additive':
        input_lines.append(f"Key (k): {key_k}")
        input_lines.append("")
        input_lines.append("Additive Cipher (also called Caesar Cipher):")
        input_lines.append("  Encryption: E(x) = (x + k) mod 26")
        input_lines.append("  Decryption: D(x) = (x - k) mod 26")
    elif mode == 'multiplicative':
        input_lines.append(f"Key (k): {key_k}")
        input_lines.append("")
        input_lines.append("Multiplicative Cipher:")
        input_lines.append("  Encryption: E(x) = (x × k) mod 26")
        input_lines.append("  Decryption: D(x) = (x × k⁻¹) mod 26")
        input_lines.append("  Requirement: k must be coprime with 26")
    else:  # affine
        input_lines.append(f"Key a: {key_a}")
        input_lines.append(f"Key b: {key_b}")
        input_lines.append("")
        input_lines.append("Affine Cipher:")
        input_lines.append("  Encryption: E(x) = (a × x + b) mod 26")
        input_lines.append("  Decryption: D(x) = a⁻¹ × (x - b) mod 26")
        input_lines.append("  Requirement: a must be coprime with 26")
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": '\n'.join(input_lines)}]
    })
    
    # Section 2: Alphabet Mapping
    mapping_lines = ["Standard Alphabet to Number Mapping (A=0 to Z=25):"]
    mapping_lines.append("")
    mapping_lines.append("A= 0  B= 1  C= 2  D= 3  E= 4  F= 5  G= 6  H= 7  I= 8  J= 9")
    mapping_lines.append("K=10  L=11  M=12  N=13  O=14  P=15  Q=16  R=17  S=18  T=19")
    mapping_lines.append("U=20  V=21  W=22  X=23  Y=24  Z=25")
    
    all_sections.append({
        "section": "Alphabet Mapping",
        "subsections": [{"title": "Character ↔ Number", "content": '\n'.join(mapping_lines)}]
    })
    
    # Section 3: Key Validation (for multiplicative and affine)
    if mode == 'multiplicative':
        valid_lines = []
        valid_lines.append(f"Checking if key k = {key_k} is valid...")
        valid_lines.append("")
        valid_lines.append(f"For Multiplicative Cipher: gcd(k, 26) must equal 1")
        valid_lines.append("")
        
        g = gcd(key_k, 26)
        valid_lines.append(f"gcd({key_k}, 26) = {g}")
        
        if g != 1:
            valid_lines.append("")
            valid_lines.append(f"✗ INVALID KEY: {key_k} is NOT coprime with 26!")
            valid_lines.append(f"  The key has no modular inverse.")
            valid_lines.append("")
            valid_lines.append("Valid keys for mod 26: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25")
            
            all_sections.append({
                "section": "Key Validation",
                "subsections": [{"title": "Coprimality Check", "content": '\n'.join(valid_lines)}]
            })
            
            return {
                "success": False,
                "error": f"Key {key_k} is not coprime with 26. Valid keys: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25",
                "sections": all_sections
            }
        else:
            valid_lines.append("")
            valid_lines.append(f"✓ VALID KEY: {key_k} is coprime with 26")
            
        all_sections.append({
            "section": "Key Validation",
            "subsections": [{"title": "Coprimality Check", "content": '\n'.join(valid_lines)}]
        })
    
    elif mode == 'affine':
        valid_lines = []
        valid_lines.append(f"Checking if key a = {key_a} is valid...")
        valid_lines.append("")
        valid_lines.append(f"For Affine Cipher: gcd(a, 26) must equal 1")
        valid_lines.append("")
        
        g = gcd(key_a, 26)
        valid_lines.append(f"gcd({key_a}, 26) = {g}")
        
        if g != 1:
            valid_lines.append("")
            valid_lines.append(f"✗ INVALID KEY: {key_a} is NOT coprime with 26!")
            valid_lines.append("")
            valid_lines.append("Valid values for 'a' (must be coprime with 26):")
            valid_lines.append("1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25")
            
            all_sections.append({
                "section": "Key Validation",
                "subsections": [{"title": "Coprimality Check", "content": '\n'.join(valid_lines)}]
            })
            
            return {
                "success": False,
                "error": f"Key 'a' ({key_a}) is not coprime with 26",
                "sections": all_sections
            }
        else:
            valid_lines.append("")
            valid_lines.append(f"✓ VALID KEY: {key_a} is coprime with 26")
        
        all_sections.append({
            "section": "Key Validation",
            "subsections": [{"title": "Coprimality Check", "content": '\n'.join(valid_lines)}]
        })
    
    # Section 4: Find Inverse (if needed for decryption)
    key_inv = None
    if operation == 'decrypt' and mode in ['multiplicative', 'affine']:
        inv_key = key_k if mode == 'multiplicative' else key_a
        
        # Method 1: Brute Force
        inv_brute, brute_steps = brute_force_inverse_detailed(inv_key, 26)
        all_sections.append({
            "section": "Finding Inverse - Method 1: Brute Force (Trial)",
            "subsections": [{"title": f"Finding {inv_key}⁻¹ mod 26", "content": brute_steps}]
        })
        
        # Method 2: Extended Euclidean
        inv_ext, ext_steps = extended_euclidean_detailed(inv_key, 26)
        all_sections.append({
            "section": "Finding Inverse - Method 2: Extended Euclidean Algorithm",
            "subsections": [{"title": f"Finding {inv_key}⁻¹ mod 26 (Efficient)", "content": ext_steps}]
        })
        
        key_inv = inv_ext
        
        # Summary
        compare_lines = []
        compare_lines.append("Comparison of Methods:")
        compare_lines.append("")
        compare_lines.append("Method 1 - Brute Force:")
        compare_lines.append("  • Tries all values from 1 to m-1")
        compare_lines.append("  • Time Complexity: O(m)")
        compare_lines.append("  • Simple but INEFFICIENT for large modulus")
        compare_lines.append("")
        compare_lines.append("Method 2 - Extended Euclidean Algorithm:")
        compare_lines.append("  • Uses division and back-substitution")
        compare_lines.append("  • Time Complexity: O(log m)")
        compare_lines.append("  • EFFICIENT even for very large numbers")
        compare_lines.append("")
        compare_lines.append(f"Both methods give: {inv_key}⁻¹ mod 26 = {key_inv}")
        
        all_sections.append({
            "section": "Method Comparison",
            "subsections": [{"title": "Brute Force vs Extended Euclidean", "content": '\n'.join(compare_lines)}]
        })
    
    # Section 5: Character-by-Character Processing
    proc_lines = []
    proc_lines.append(f"Processing each character of \"{plaintext}\":")
    proc_lines.append("")
    
    result = ""
    
    for idx, char in enumerate(plaintext):
        if not char.isalpha():
            continue
        
        x = ord(char.lower()) - ord('a')
        proc_lines.append(f"Character {idx + 1}: '{char}'")
        proc_lines.append(f"  Numeric value: {char.lower()} → {x}")
        
        if mode == 'additive':
            if operation == 'encrypt':
                # E(x) = (x + k) mod 26
                y = (x + key_k) % 26
                proc_lines.append(f"  Formula: E(x) = (x + k) mod 26")
                proc_lines.append(f"  Calculation: ({x} + {key_k}) mod 26")
                proc_lines.append(f"             = {x + key_k} mod 26")
                proc_lines.append(f"             = {y}")
            else:
                # D(x) = (x - k) mod 26
                y = (x - key_k) % 26
                proc_lines.append(f"  Formula: D(x) = (x - k) mod 26")
                proc_lines.append(f"  Calculation: ({x} - {key_k}) mod 26")
                proc_lines.append(f"             = {x - key_k} mod 26")
                proc_lines.append(f"             = {y}")
        
        elif mode == 'multiplicative':
            if operation == 'encrypt':
                # E(x) = (x × k) mod 26
                y = (x * key_k) % 26
                proc_lines.append(f"  Formula: E(x) = (x × k) mod 26")
                proc_lines.append(f"  Calculation: ({x} × {key_k}) mod 26")
                proc_lines.append(f"             = {x * key_k} mod 26")
                proc_lines.append(f"             = {y}")
            else:
                # D(x) = (x × k⁻¹) mod 26
                y = (x * key_inv) % 26
                proc_lines.append(f"  Formula: D(x) = (x × k⁻¹) mod 26")
                proc_lines.append(f"  Calculation: ({x} × {key_inv}) mod 26")
                proc_lines.append(f"             = {x * key_inv} mod 26")
                proc_lines.append(f"             = {y}")
        
        else:  # affine
            if operation == 'encrypt':
                # E(x) = (a × x + b) mod 26
                y = (key_a * x + key_b) % 26
                proc_lines.append(f"  Formula: E(x) = (a × x + b) mod 26")
                proc_lines.append(f"  Calculation: ({key_a} × {x} + {key_b}) mod 26")
                proc_lines.append(f"             = ({key_a * x} + {key_b}) mod 26")
                proc_lines.append(f"             = {key_a * x + key_b} mod 26")
                proc_lines.append(f"             = {y}")
            else:
                # D(x) = a⁻¹ × (x - b) mod 26
                y = (key_inv * (x - key_b)) % 26
                proc_lines.append(f"  Formula: D(x) = a⁻¹ × (x - b) mod 26")
                proc_lines.append(f"  Calculation: {key_inv} × ({x} - {key_b}) mod 26")
                proc_lines.append(f"             = {key_inv} × {x - key_b} mod 26")
                proc_lines.append(f"             = {key_inv * (x - key_b)} mod 26")
                proc_lines.append(f"             = {y}")
        
        result_char = chr(y + ord('a'))
        result += result_char
        proc_lines.append(f"  Result: {y} → '{result_char}'")
        proc_lines.append("")
    
    all_sections.append({
        "section": f"{operation.capitalize()}ion Process",
        "subsections": [{"title": "Character-by-Character Transformation", "content": '\n'.join(proc_lines)}]
    })
    
    # Section 6: Final Result
    result_lines = []
    result_lines.append(f"MONOALPHABETIC CIPHER ({mode.upper()}) COMPLETE")
    result_lines.append("")
    result_lines.append(f"Input:     \"{plaintext}\"")
    result_lines.append(f"Operation: {operation.upper()}")
    if mode == 'additive':
        result_lines.append(f"Key (k):   {key_k}")
    elif mode == 'multiplicative':
        result_lines.append(f"Key (k):   {key_k}")
        if operation == 'decrypt':
            result_lines.append(f"Key⁻¹:     {key_inv}")
    else:
        result_lines.append(f"Key (a):   {key_a}")
        result_lines.append(f"Key (b):   {key_b}")
        if operation == 'decrypt':
            result_lines.append(f"a⁻¹:       {key_inv}")
    result_lines.append("")
    result_lines.append(f"★ OUTPUT: \"{result.upper()}\"")
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Summary", "content": '\n'.join(result_lines)}]
    })
    
    return {
        "success": True,
        "plaintext": plaintext,
        "mode": mode,
        "operation": operation,
        "result": result.upper(),
        "sections": all_sections
    }


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
        self.wfile.write(json.dumps({"status": "Monoalphabetic Cipher API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            plaintext = data.get('plaintext', 'hello')
            mode = data.get('mode', 'additive')  # additive, multiplicative, affine
            operation = data.get('operation', 'encrypt')  # encrypt, decrypt
            key_k = data.get('key_k', 3)
            key_a = data.get('key_a', 5)
            key_b = data.get('key_b', 8)
            
            result = monoalphabetic_cipher_detailed(
                plaintext, mode, key_k=key_k, key_a=key_a, key_b=key_b, operation=operation
            )
            
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
