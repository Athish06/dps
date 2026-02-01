from http.server import BaseHTTPRequestHandler
import json

def mod_exp_detailed(a, n, m):
    """Modular Exponentiation using repeated squaring with detailed steps"""
    all_sections = []
    
    # Section 1: Input Parameters
    input_content = f"""Given:
  Base a = {a}
  Exponent n = {n}
  Modulus m = {m}

Goal: Compute {a}^{n} mod {m}

Method: Fast Exponentiation (Square-and-Multiply / Repeated Squaring)"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": input_content}]
    })
    
    # Section 2: Binary Expansion
    binary = bin(n)[2:]  # Remove '0b' prefix
    bin_lines = []
    bin_lines.append("═" * 55)
    bin_lines.append("BINARY EXPANSION OF EXPONENT")
    bin_lines.append("═" * 55)
    bin_lines.append("")
    bin_lines.append(f"n = {n}")
    bin_lines.append(f"n in binary = {binary}")
    bin_lines.append("")
    bin_lines.append("Binary digits (right to left):")
    bin_lines.append("")
    
    # Show binary breakdown
    power_of_2 = 1
    for i, bit in enumerate(reversed(binary)):
        if bit == '1':
            bin_lines.append(f"  Position {i}: 2^{i} = {power_of_2} ✓ (bit = 1)")
        else:
            bin_lines.append(f"  Position {i}: 2^{i} = {power_of_2} ✗ (bit = 0)")
        power_of_2 *= 2
    
    bin_lines.append("")
    bin_lines.append(f"Number of bits: {len(binary)}")
    bin_lines.append(f"Number of 1-bits: {binary.count('1')}")
    
    all_sections.append({
        "section": "Binary Expansion",
        "subsections": [{"title": f"n = {binary} (binary)", "content": '\n'.join(bin_lines)}]
    })
    
    # Section 3: Repeated Squaring Algorithm
    sq_lines = []
    sq_lines.append("═" * 55)
    sq_lines.append("REPEATED SQUARING ALGORITHM")
    sq_lines.append("═" * 55)
    sq_lines.append("")
    sq_lines.append("Algorithm:")
    sq_lines.append("  1. Start with result = 1, base = a mod m")
    sq_lines.append("  2. For each bit of n (right to left):")
    sq_lines.append("     - If bit == 1: result = (result × base) mod m")
    sq_lines.append("     - Square the base: base = (base × base) mod m")
    sq_lines.append("")
    sq_lines.append("─" * 55)
    sq_lines.append("")
    
    result = 1
    base = a % m
    bit_position = 0
    
    sq_lines.append(f"Initial: result = 1, base = {a} mod {m} = {base}")
    sq_lines.append("")
    
    temp_n = n
    while temp_n > 0:
        bit = temp_n & 1
        sq_lines.append(f"Step {bit_position + 1}: Processing bit {bit_position}")
        sq_lines.append(f"  Current bit = {bit}")
        sq_lines.append(f"  Binary position = 2^{bit_position} = {2**bit_position}")
        sq_lines.append("")
        
        if bit == 1:
            old_result = result
            result = (result * base) % m
            sq_lines.append(f"  Bit = 1, so multiply:")
            sq_lines.append(f"    result = result × base mod {m}")
            sq_lines.append(f"    result = {old_result} × {base} mod {m}")
            sq_lines.append(f"    result = {old_result * base} mod {m}")
            sq_lines.append(f"    result = {result}")
        else:
            sq_lines.append(f"  Bit = 0, so skip multiplication")
            sq_lines.append(f"    result = {result} (unchanged)")
        
        sq_lines.append("")
        
        old_base = base
        base = (base * base) % m
        sq_lines.append(f"  Square the base for next iteration:")
        sq_lines.append(f"    base = base × base mod {m}")
        sq_lines.append(f"    base = {old_base} × {old_base} mod {m}")
        sq_lines.append(f"    base = {old_base * old_base} mod {m}")
        sq_lines.append(f"    base = {base}")
        sq_lines.append("")
        sq_lines.append("─" * 55)
        sq_lines.append("")
        
        temp_n >>= 1
        bit_position += 1
    
    all_sections.append({
        "section": "Repeated Squaring Steps",
        "subsections": [{"title": "Square-and-Multiply Algorithm", "content": '\n'.join(sq_lines)}]
    })
    
    # Section 4: Result
    result_lines = []
    result_lines.append("═" * 55)
    result_lines.append("FINAL RESULT")
    result_lines.append("═" * 55)
    result_lines.append("")
    result_lines.append(f"<b>★ {a}^{n} mod {m} = {result}</b>")
    result_lines.append("")
    result_lines.append(f"Computation Efficiency:")
    result_lines.append(f"  - Without optimization: {n} multiplications")
    result_lines.append(f"  - With repeated squaring: {len(binary)} squarings + {binary.count('1')} multiplications")
    result_lines.append(f"  - Total operations: ~{len(binary) + binary.count('1')}")
    result_lines.append("")
    result_lines.append("═" * 55)
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Answer", "content": '\n'.join(result_lines)}]
    })
    
    return {
        "success": True,
        "result": result,
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
        self.wfile.write(json.dumps({"status": "Modular Exponentiation API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            a = int(data.get('a', 7))
            n = int(data.get('n', 256))
            m = int(data.get('m', 13))
            
            result = mod_exp_detailed(a, n, m)
            
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
