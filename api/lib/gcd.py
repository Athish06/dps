from http.server import BaseHTTPRequestHandler
import json

def gcd_detailed(a, b):
    """Euclidean Algorithm for GCD with detailed steps"""
    all_sections = []
    
    original_a, original_b = a, b
    
    # Section 1: Input Parameters
    input_content = f"""Given:
  a = {a}
  b = {b}

Goal: Find GCD({a}, {b}) using Euclidean Algorithm

Euclidean Algorithm Principle:
  GCD(a, b) = GCD(b, a mod b)
  Continue until remainder = 0"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": input_content}]
    })
    
    # Section 2: Euclidean Algorithm Steps
    lines = []
    lines.append("═" * 55)
    lines.append("EUCLIDEAN ALGORITHM")
    lines.append("═" * 55)
    lines.append("")
    lines.append("Formula: a = b × q + r")
    lines.append("         GCD(a, b) = GCD(b, r)")
    lines.append("")
    lines.append("─" * 55)
    lines.append("")
    
    step = 1
    steps_data = []
    
    # Ensure a >= b for cleaner output
    if a < b:
        a, b = b, a
        lines.append(f"Swap so that a ≥ b: a = {a}, b = {b}")
        lines.append("")
    
    while b != 0:
        q = a // b
        r = a % b
        
        lines.append(f"Step {step}:")
        lines.append(f"  a = {a}, b = {b}")
        lines.append(f"  q = a ÷ b = {a} ÷ {b} = {q}")
        lines.append(f"  r = a - b × q = {a} - {b} × {q} = {a} - {b * q} = {r}")
        lines.append("")
        lines.append(f"  Division: {a} = {b} × {q} + {r}")
        lines.append(f"  Therefore: GCD({a}, {b}) = GCD({b}, {r})")
        lines.append("")
        
        steps_data.append({
            'step': step, 'a': a, 'b': b, 'q': q, 'r': r
        })
        
        a, b = b, r
        step += 1
        lines.append("─" * 55)
        lines.append("")
    
    lines.append(f"Remainder = 0, algorithm terminates.")
    lines.append(f"GCD = {a} (the last non-zero remainder)")
    
    all_sections.append({
        "section": "Euclidean Algorithm Steps",
        "subsections": [{"title": "Step-by-Step Division", "content": '\n'.join(lines)}]
    })
    
    gcd = a
    
    # Section 3: Summary Table
    table_lines = []
    table_lines.append("═" * 55)
    table_lines.append("COMPUTATION TABLE")
    table_lines.append("═" * 55)
    table_lines.append("")
    table_lines.append("Step │   a   │   b   │   q   │   r")
    table_lines.append("─────┼───────┼───────┼───────┼───────")
    
    for s in steps_data:
        table_lines.append(f"  {s['step']}  │ {s['a']:>5} │ {s['b']:>5} │ {s['q']:>5} │ {s['r']:>5}")
    
    table_lines.append("─────┴───────┴───────┴───────┴───────")
    table_lines.append("")
    table_lines.append(f"Last non-zero value in 'b' column before r=0: {gcd}")
    
    all_sections.append({
        "section": "Summary Table",
        "subsections": [{"title": "All Steps", "content": '\n'.join(table_lines)}]
    })
    
    # Section 4: Coprimality Check
    coprime_lines = []
    coprime_lines.append("═" * 55)
    coprime_lines.append("COPRIMALITY CHECK")
    coprime_lines.append("═" * 55)
    coprime_lines.append("")
    coprime_lines.append(f"Two numbers are coprime (relatively prime) if GCD = 1")
    coprime_lines.append("")
    coprime_lines.append(f"GCD({original_a}, {original_b}) = {gcd}")
    coprime_lines.append("")
    
    if gcd == 1:
        coprime_lines.append(f"Since GCD = 1:")
        coprime_lines.append(f"  ★ {original_a} and {original_b} ARE COPRIME!")
        coprime_lines.append("")
        coprime_lines.append("This means:")
        coprime_lines.append(f"  • {original_a} and {original_b} share no common factors (except 1)")
        coprime_lines.append(f"  • Multiplicative inverse of {original_a} mod {original_b} EXISTS")
        coprime_lines.append(f"  • In RSA: e and φ(n) must be coprime for valid key")
    else:
        coprime_lines.append(f"Since GCD = {gcd} ≠ 1:")
        coprime_lines.append(f"  ✗ {original_a} and {original_b} are NOT coprime")
        coprime_lines.append("")
        coprime_lines.append(f"Common factors exist:")
        coprime_lines.append(f"  • {original_a} = {gcd} × {original_a // gcd}")
        coprime_lines.append(f"  • {original_b} = {gcd} × {original_b // gcd}")
        coprime_lines.append("")
        coprime_lines.append(f"  ✗ NO multiplicative inverse exists for {original_a} mod {original_b}")
    
    coprime_lines.append("")
    coprime_lines.append("═" * 55)
    
    all_sections.append({
        "section": "Coprimality Check",
        "subsections": [{"title": "Are they coprime?", "content": '\n'.join(coprime_lines)}]
    })
    
    # Section 5: Final Result
    result_lines = []
    result_lines.append("═" * 55)
    result_lines.append("FINAL RESULT")
    result_lines.append("═" * 55)
    result_lines.append("")
    result_lines.append(f"<b>★ GCD({original_a}, {original_b}) = {gcd}</b>")
    result_lines.append("")
    result_lines.append(f"Coprime: {'Yes ✓' if gcd == 1 else 'No ✗'}")
    result_lines.append("")
    result_lines.append(f"Number of steps: {len(steps_data)}")
    result_lines.append("")
    result_lines.append("═" * 55)
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Answer", "content": '\n'.join(result_lines)}]
    })
    
    return {
        "success": True,
        "gcd": gcd,
        "coprime": gcd == 1,
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
        self.wfile.write(json.dumps({"status": "GCD Calculator API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            a = int(data.get('a', 48))
            b = int(data.get('b', 18))
            
            result = gcd_detailed(a, b)
            
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
