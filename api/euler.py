from http.server import BaseHTTPRequestHandler
import json
import math

def get_gcd(a, b):
    """Calculate GCD using Euclidean algorithm"""
    while b:
        a, b = b, a % b
    return a

def calculate_totient_detailed(n):
    """Calculate Euler's Totient φ(n) with detailed steps"""
    lines = []
    lines.append("═" * 55)
    lines.append(f"CALCULATING EULER'S TOTIENT φ({n})")
    lines.append("═" * 55)
    lines.append("")
    lines.append("Formula: φ(n) = n × ∏(1 - 1/p) for each prime factor p")
    lines.append("")
    lines.append("Algorithm:")
    lines.append("  1. Start with result = n")
    lines.append("  2. Find all prime factors p of n")
    lines.append("  3. For each prime p: result = result - result/p")
    lines.append("")
    lines.append("─" * 55)
    lines.append("")
    
    result = n
    original_n = n
    p = 2
    temp_n = n
    prime_factors = []
    
    lines.append(f"Initial: result = {result}")
    lines.append("")
    
    # Find prime factors
    step = 1
    while p * p <= temp_n:
        if temp_n % p == 0:
            prime_factors.append(p)
            lines.append(f"Step {step}: Check if {p} divides {temp_n}")
            lines.append(f"  {temp_n} ÷ {p} = {temp_n // p} (remainder {temp_n % p})")
            lines.append(f"  ✓ {p} is a prime factor!")
            lines.append("")
            
            # Remove all occurrences of p
            count = 0
            while temp_n % p == 0:
                temp_n //= p
                count += 1
            
            lines.append(f"  Factor {p} appears {count} time(s)")
            lines.append(f"  After removing: temp_n = {temp_n}")
            lines.append("")
            
            # Update result
            old_result = result
            result -= result // p
            lines.append(f"  Update φ: result = result - result/{p}")
            lines.append(f"          = {old_result} - {old_result // p}")
            lines.append(f"          = {result}")
            lines.append("")
            lines.append("─" * 55)
            lines.append("")
            step += 1
        p += 1
    
    # If remaining temp_n > 1, it's a prime factor
    if temp_n > 1:
        prime_factors.append(temp_n)
        lines.append(f"Step {step}: Remaining value {temp_n} > 1")
        lines.append(f"  ✓ {temp_n} is a prime factor!")
        lines.append("")
        
        old_result = result
        result -= result // temp_n
        lines.append(f"  Update φ: result = result - result/{temp_n}")
        lines.append(f"          = {old_result} - {old_result // temp_n}")
        lines.append(f"          = {result}")
        lines.append("")
        lines.append("─" * 55)
        lines.append("")
    
    lines.append("SUMMARY:")
    lines.append(f"  Prime factors of {original_n}: {prime_factors}")
    lines.append(f"  <b>φ({original_n}) = {result}</b>")
    lines.append("")
    
    return result, '\n'.join(lines)

def euler_theorem_detailed(base, exponent, modulus):
    """Euler's Theorem solver with detailed steps"""
    all_sections = []
    
    # Section 1: Input Parameters
    input_content = f"""Given:
  Base a = {base}
  Exponent b = {exponent}
  Modulus n = {modulus}

Goal: Compute {base}^{exponent} mod {modulus}

Euler's Theorem:
  If gcd(a, n) = 1, then a^φ(n) ≡ 1 (mod n)
  
This allows us to reduce large exponents:
  a^b mod n = a^(b mod φ(n)) mod n"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Euler's Theorem", "content": input_content}]
    })
    
    # Section 2: GCD Check
    gcd_lines = []
    gcd_lines.append("═" * 55)
    gcd_lines.append("STEP 1: CHECK IF GCD(a, n) = 1")
    gcd_lines.append("═" * 55)
    gcd_lines.append("")
    gcd_lines.append("For Euler's Theorem to apply, a and n must be coprime.")
    gcd_lines.append("")
    
    gcd_value = get_gcd(base, modulus)
    
    # Show GCD calculation steps
    a, b = modulus, base % modulus
    gcd_lines.append("Using Euclidean Algorithm:")
    gcd_lines.append(f"  gcd({base}, {modulus}):")
    
    temp_a, temp_b = modulus, base % modulus
    while temp_b:
        gcd_lines.append(f"    {temp_a} = {temp_b} × {temp_a // temp_b} + {temp_a % temp_b}")
        temp_a, temp_b = temp_b, temp_a % temp_b
    
    gcd_lines.append("")
    gcd_lines.append(f"  gcd({base}, {modulus}) = {gcd_value}")
    gcd_lines.append("")
    
    if gcd_value != 1:
        gcd_lines.append(f"⚠️ GCD = {gcd_value} ≠ 1")
        gcd_lines.append("")
        gcd_lines.append("Since a and n are NOT coprime,")
        gcd_lines.append("Euler's theorem (a^φ(n) ≡ 1) does NOT strictly apply!")
        gcd_lines.append("")
        gcd_lines.append("Falling back to standard modular exponentiation...")
        
        all_sections.append({
            "section": "GCD Check",
            "subsections": [{"title": "Coprimality Test", "content": '\n'.join(gcd_lines)}]
        })
        
        # Fallback calculation
        result = pow(base, exponent, modulus)
        
        fallback_lines = []
        fallback_lines.append("═" * 55)
        fallback_lines.append("FALLBACK: STANDARD MODULAR EXPONENTIATION")
        fallback_lines.append("═" * 55)
        fallback_lines.append("")
        fallback_lines.append(f"Using Python's built-in pow({base}, {exponent}, {modulus})")
        fallback_lines.append("")
        fallback_lines.append(f"<b>★ {base}^{exponent} mod {modulus} = {result}</b>")
        fallback_lines.append("")
        
        all_sections.append({
            "section": "Final Result",
            "subsections": [{"title": "Answer", "content": '\n'.join(fallback_lines)}]
        })
        
        return {
            "success": True,
            "result": result,
            "euler_applied": False,
            "sections": all_sections
        }
    
    gcd_lines.append("✓ GCD = 1 (Coprime!)")
    gcd_lines.append("")
    gcd_lines.append("Euler's Theorem applies! We can reduce the exponent.")
    
    all_sections.append({
        "section": "GCD Check",
        "subsections": [{"title": "Coprimality Test", "content": '\n'.join(gcd_lines)}]
    })
    
    # Section 3: Calculate Totient
    phi_n, phi_detail = calculate_totient_detailed(modulus)
    
    all_sections.append({
        "section": "Calculate φ(n)",
        "subsections": [{"title": f"Euler's Totient of {modulus}", "content": phi_detail}]
    })
    
    # Section 4: Reduce Exponent
    reduce_lines = []
    reduce_lines.append("═" * 55)
    reduce_lines.append("STEP 2: REDUCE THE EXPONENT")
    reduce_lines.append("═" * 55)
    reduce_lines.append("")
    reduce_lines.append("By Euler's Theorem: a^φ(n) ≡ 1 (mod n)")
    reduce_lines.append("")
    reduce_lines.append("Therefore: a^b ≡ a^(b mod φ(n)) (mod n)")
    reduce_lines.append("")
    reduce_lines.append("─" * 55)
    reduce_lines.append("")
    reduce_lines.append(f"Original exponent: b = {exponent}")
    reduce_lines.append(f"φ({modulus}) = {phi_n}")
    reduce_lines.append("")
    reduce_lines.append(f"New exponent = {exponent} mod {phi_n}")
    
    reduced_exp = exponent % phi_n
    
    reduce_lines.append(f"             = {exponent} ÷ {phi_n} = {exponent // phi_n} remainder {reduced_exp}")
    reduce_lines.append(f"             = {reduced_exp}")
    reduce_lines.append("")
    reduce_lines.append(f"<b>Reduced problem: {base}^{reduced_exp} mod {modulus}</b>")
    reduce_lines.append("")
    reduce_lines.append("This is MUCH easier to compute!")
    if exponent > 1000:
        reduce_lines.append(f"(Reduced from {exponent} to just {reduced_exp})")
    
    all_sections.append({
        "section": "Reduce Exponent",
        "subsections": [{"title": "Using Euler's Theorem", "content": '\n'.join(reduce_lines)}]
    })
    
    # Section 5: Final Calculation
    calc_lines = []
    calc_lines.append("═" * 55)
    calc_lines.append("STEP 3: FINAL CALCULATION")
    calc_lines.append("═" * 55)
    calc_lines.append("")
    calc_lines.append(f"Compute: {base}^{reduced_exp} mod {modulus}")
    calc_lines.append("")
    
    # Show step-by-step if small enough
    if reduced_exp <= 20:
        calc_lines.append("Step-by-step multiplication:")
        calc_lines.append("")
        current = 1
        for i in range(reduced_exp):
            old_current = current
            current = (current * base) % modulus
            calc_lines.append(f"  Step {i+1}: {old_current} × {base} mod {modulus} = {current}")
        calc_lines.append("")
    else:
        calc_lines.append(f"Using fast modular exponentiation:")
        calc_lines.append(f"  pow({base}, {reduced_exp}, {modulus})")
        calc_lines.append("")
    
    result = pow(base, reduced_exp, modulus)
    
    calc_lines.append("─" * 55)
    calc_lines.append("")
    calc_lines.append(f"<b>★ {base}^{exponent} mod {modulus} = {result}</b>")
    calc_lines.append("")
    calc_lines.append("Verification:")
    calc_lines.append(f"  {base}^{reduced_exp} mod {modulus} = {result} ✓")
    calc_lines.append("")
    calc_lines.append("═" * 55)
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Answer", "content": '\n'.join(calc_lines)}]
    })
    
    return {
        "success": True,
        "result": result,
        "euler_applied": True,
        "phi_n": phi_n,
        "reduced_exponent": reduced_exp,
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
        self.wfile.write(json.dumps({"status": "Euler's Theorem API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            base = int(data.get('base', 7))
            exponent = int(data.get('exponent', 256))
            modulus = int(data.get('modulus', 13))
            
            result = euler_theorem_detailed(base, exponent, modulus)
            
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