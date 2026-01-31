from http.server import BaseHTTPRequestHandler
import json

def extended_euclidean_detailed(a, m):
    """Extended Euclidean Algorithm with Fast Guess Method"""
    all_sections = []
    
    # Section 1: Input Parameters
    input_content = f"""Given:
  a = {a}
  m = {m}

Goal: Find GCD(a, m) and multiplicative inverse of a mod m
      (i.e., find d such that a × d ≡ 1 (mod m))"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": input_content}]
    })
    
    # Section 2: Extended Euclidean Algorithm
    lines = []
    lines.append("═" * 55)
    lines.append("EXTENDED EUCLIDEAN ALGORITHM")
    lines.append(f"Finding GCD({a}, {m}) and coefficients s, t")
    lines.append(f"such that: {a}×s + {m}×t = GCD({a}, {m})")
    lines.append("═" * 55)
    lines.append("")
    
    # Formulas
    lines.append("FORMULAS:")
    lines.append("─" * 40)
    lines.append("Recurrence Relations:")
    lines.append("  q = r1 ÷ r2  (integer division)")
    lines.append("  r = r1 - q × r2  (remainder)")
    lines.append("  s = s1 - q × s2")
    lines.append("  t = t1 - q × t2")
    lines.append("")
    lines.append("Init: s1=1, s2=0, t1=0, t2=1")
    lines.append("─" * 40)
    lines.append("")
    
    # Initialize values
    r1, r2 = m, a
    s1, s2 = 1, 0
    t1, t2 = 0, 1
    
    # Computation table
    lines.append("COMPUTATION TABLE:")
    lines.append("─" * 50)
    lines.append("  q  │  r1  │  r2  │  r  │  s  │  t")
    lines.append("─────┼──────┼──────┼─────┼─────┼─────")
    lines.append(f"  -  │ {r1:>4} │ {r2:>4} │  -  │  -  │  -   ← Init")
    
    step = 1
    calculation_steps = []
    
    while r2 > 0:
        q = r1 // r2
        r = r1 % r2
        s = s1 - (q * s2)
        t = t1 - (q * t2)
        
        calc_detail = {
            'step': step, 'q': q, 'r1': r1, 'r2': r2, 'r': r,
            's1': s1, 's2': s2, 's': s, 't1': t1, 't2': t2, 't': t
        }
        calculation_steps.append(calc_detail)
        
        lines.append(f" {q:>2}  │ {r1:>4} │ {r2:>4} │ {r:>3} │ {s:>3} │ {t:>3}   Step {step}")
        
        r1, r2 = r2, r
        s1, s2 = s2, s
        t1, t2 = t2, t
        step += 1
    
    lines.append("─" * 50)
    gcd = r1
    lines.append(f"GCD({a}, {m}) = {gcd}")
    lines.append("")
    
    # Detailed calculations
    lines.append("DETAILED CALCULATIONS:")
    lines.append("═" * 55)
    
    for calc in calculation_steps:
        lines.append("")
        lines.append(f"STEP {calc['step']}")
        lines.append("─" * 55)
        lines.append(f"Given: r1={calc['r1']}, r2={calc['r2']}, s1={calc['s1']}, s2={calc['s2']}, t1={calc['t1']}, t2={calc['t2']}")
        lines.append("")
        lines.append("Calculate q (quotient):")
        lines.append(f"  q = r1 ÷ r2 = {calc['r1']} ÷ {calc['r2']} = {calc['q']}")
        lines.append("")
        lines.append("Calculate r (remainder):")
        lines.append(f"  r = r1 - q × r2")
        lines.append(f"  r = {calc['r1']} - {calc['q']} × {calc['r2']}")
        lines.append(f"  r = {calc['r1']} - {calc['q'] * calc['r2']} = {calc['r']}")
        lines.append("")
        lines.append("Calculate s:")
        lines.append(f"  s = s1 - q × s2")
        lines.append(f"  s = {calc['s1']} - {calc['q']} × {calc['s2']}")
        lines.append(f"  s = {calc['s1']} - ({calc['q'] * calc['s2']}) = {calc['s']}")
        lines.append("")
        lines.append("Calculate t:")
        lines.append(f"  t = t1 - q × t2")
        lines.append(f"  t = {calc['t1']} - {calc['q']} × {calc['t2']}")
        lines.append(f"  t = {calc['t1']} - ({calc['q'] * calc['t2']}) = {calc['t']}")
        lines.append("")
        lines.append("Update for next step:")
        lines.append(f"  r1 ← r2 = {calc['r2']},  r2 ← r = {calc['r']}")
        lines.append(f"  s1 ← s2 = {calc['s2']},  s2 ← s = {calc['s']}")
        lines.append(f"  t1 ← t2 = {calc['t2']},  t2 ← t = {calc['t']}")
        lines.append("─" * 55)
    
    all_sections.append({
        "section": "Extended Euclidean Algorithm",
        "subsections": [{"title": "Step-by-Step Calculation", "content": '\n'.join(lines)}]
    })
    
    # Section 3: Fast Guess Method (if applicable)
    if gcd == 1:
        fast_lines = []
        fast_lines.append("═" * 55)
        fast_lines.append("FAST GUESS METHOD")
        fast_lines.append("═" * 55)
        fast_lines.append("")
        fast_lines.append("Alternative method to find inverse (trial approach):")
        fast_lines.append(f"We need d such that: {a} × d ≡ 1 (mod {m})")
        fast_lines.append("")
        fast_lines.append("Starting guess: d = 1, then increment...")
        fast_lines.append("")
        
        # Find inverse by trial
        for trial in range(1, min(m, 50) + 1):
            result = (a * trial) % m
            if result == 1:
                fast_lines.append(f"  Try d = {trial}:")
                fast_lines.append(f"    {a} × {trial} = {a * trial}")
                fast_lines.append(f"    {a * trial} mod {m} = {result} ✓")
                fast_lines.append("")
                fast_lines.append(f"★ Found! d = {trial}")
                break
            elif trial <= 10 or trial == min(m, 50):
                fast_lines.append(f"  Try d = {trial}: {a} × {trial} = {a * trial}, mod {m} = {result} ✗")
            elif trial == 11:
                fast_lines.append(f"  ...")
        
        all_sections.append({
            "section": "Fast Guess Method",
            "subsections": [{"title": "Trial Division Approach", "content": '\n'.join(fast_lines)}]
        })
    
    # Section 4: Result
    result_lines = []
    result_lines.append("═" * 55)
    result_lines.append("RESULT")
    result_lines.append("═" * 55)
    result_lines.append("")
    result_lines.append(f"GCD({a}, {m}) = {gcd}")
    result_lines.append("")
    
    if gcd == 1:
        inverse = t1
        if inverse < 0:
            result_lines.append(f"Coefficient t = {inverse} (negative)")
            result_lines.append(f"Adjusting: {inverse} + {m} = {inverse + m}")
            inverse = inverse + m
        result_lines.append("")
        result_lines.append(f"<b>★ Multiplicative Inverse of {a} mod {m} = {inverse}</b>")
        result_lines.append("")
        result_lines.append("Bézout Coefficients:")
        result_lines.append(f"  s = {s1}, t = {t1 if t1 >= 0 else inverse}")
        result_lines.append(f"  {a} × {inverse} + {m} × {s1} = {a * inverse + m * s1}")
        result_lines.append("")
        result_lines.append("Verification:")
        result_lines.append(f"  {a} × {inverse} = {a * inverse}")
        result_lines.append(f"  {a * inverse} mod {m} = {(a * inverse) % m} ✓")
    else:
        result_lines.append(f"Since GCD({a}, {m}) = {gcd} ≠ 1,")
        result_lines.append(f"{a} and {m} are NOT coprime!")
        result_lines.append("")
        result_lines.append("<b>★ NO MULTIPLICATIVE INVERSE EXISTS</b>")
    
    result_lines.append("═" * 55)
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Summary", "content": '\n'.join(result_lines)}]
    })
    
    return {
        "success": True,
        "gcd": gcd,
        "inverse": (t1 % m) if gcd == 1 else None,
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
        self.wfile.write(json.dumps({"status": "Extended Euclidean API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            a = int(data.get('a', 5))
            m = int(data.get('m', 192))
            
            result = extended_euclidean_detailed(a, m)
            
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
