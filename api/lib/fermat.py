from http.server import BaseHTTPRequestHandler
import json

def is_prime(n):
    """Check if n is a prime number"""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def is_prime_detailed(n):
    """Check if n is prime with detailed steps"""
    lines = []
    lines.append("═" * 55)
    lines.append(f"PRIMALITY TEST FOR {n}")
    lines.append("═" * 55)
    lines.append("")
    
    if n <= 1:
        lines.append(f"{n} ≤ 1, so NOT PRIME")
        return False, '\n'.join(lines)
    
    if n <= 3:
        lines.append(f"{n} ∈ {{2, 3}}, so PRIME")
        return True, '\n'.join(lines)
    
    lines.append(f"Step 1: Check if {n} is divisible by 2")
    if n % 2 == 0:
        lines.append(f"  {n} ÷ 2 = {n // 2} (remainder 0)")
        lines.append(f"  ✗ {n} is divisible by 2, NOT PRIME")
        return False, '\n'.join(lines)
    lines.append(f"  {n} ÷ 2 = {n // 2} (remainder {n % 2})")
    lines.append(f"  ✓ Not divisible by 2")
    lines.append("")
    
    lines.append(f"Step 2: Check if {n} is divisible by 3")
    if n % 3 == 0:
        lines.append(f"  {n} ÷ 3 = {n // 3} (remainder 0)")
        lines.append(f"  ✗ {n} is divisible by 3, NOT PRIME")
        return False, '\n'.join(lines)
    lines.append(f"  {n} ÷ 3 = {n // 3} (remainder {n % 3})")
    lines.append(f"  ✓ Not divisible by 3")
    lines.append("")
    
    # Check using 6k±1 optimization
    lines.append(f"Step 3: Check divisibility by 6k±1 up to √{n}")
    lines.append(f"  √{n} ≈ {int(n**0.5)}")
    lines.append("")
    
    i = 5
    step = 4
    found_factor = False
    while i * i <= n:
        if n % i == 0:
            lines.append(f"  Check {i}: {n} ÷ {i} = {n // i} (remainder 0)")
            lines.append(f"  ✗ {n} is divisible by {i}, NOT PRIME")
            return False, '\n'.join(lines)
        if n % (i + 2) == 0:
            lines.append(f"  Check {i+2}: {n} ÷ {i+2} = {n // (i+2)} (remainder 0)")
            lines.append(f"  ✗ {n} is divisible by {i+2}, NOT PRIME")
            return False, '\n'.join(lines)
        if i <= 23:  # Only show first few checks
            lines.append(f"  Check {i}: {n} mod {i} = {n % i} ✓")
            lines.append(f"  Check {i+2}: {n} mod {i+2} = {n % (i+2)} ✓")
        elif i == 29:
            lines.append("  ...")
        i += 6
    
    lines.append("")
    lines.append(f"No factors found. <b>✓ {n} IS PRIME</b>")
    return True, '\n'.join(lines)


def fermat_theorem_detailed(base, exponent, modulus):
    """Fermat's Little Theorem solver with detailed steps"""
    all_sections = []
    
    # Section 1: Input Parameters
    input_content = f"""Given:
  Base a = {base}
  Exponent E = {exponent}
  Modulus p = {modulus}

Goal: Compute {base}^{exponent} mod {modulus}

Fermat's Little Theorem:
  If p is PRIME and gcd(a, p) = 1, then:
  a^(p-1) ≡ 1 (mod p)

This allows us to reduce large exponents:
  a^E mod p = a^(E mod (p-1)) mod p"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Fermat's Little Theorem", "content": input_content}]
    })
    
    # Section 2: Primality Check
    is_p_prime, prime_detail = is_prime_detailed(modulus)
    
    all_sections.append({
        "section": "Step 1: Primality Check",
        "subsections": [{"title": f"Is {modulus} prime?", "content": prime_detail}]
    })
    
    if not is_p_prime:
        # Cannot use Fermat's theorem
        error_lines = []
        error_lines.append("═" * 55)
        error_lines.append("⚠️ FERMAT'S THEOREM CANNOT BE APPLIED")
        error_lines.append("═" * 55)
        error_lines.append("")
        error_lines.append(f"The modulus p = {modulus} is NOT prime.")
        error_lines.append("")
        error_lines.append("Fermat's Little Theorem requires a PRIME modulus.")
        error_lines.append("")
        error_lines.append("Alternative: Use Euler's Theorem for non-prime moduli.")
        error_lines.append("  Euler's: a^φ(n) ≡ 1 (mod n) when gcd(a,n) = 1")
        error_lines.append("")
        error_lines.append("─" * 55)
        error_lines.append("")
        error_lines.append("Falling back to standard modular exponentiation...")
        error_lines.append("")
        
        result = pow(base, exponent, modulus)
        error_lines.append(f"<b>★ {base}^{exponent} mod {modulus} = {result}</b>")
        error_lines.append("")
        error_lines.append("(Computed using fast modular exponentiation)")
        
        all_sections.append({
            "section": "Final Result",
            "subsections": [{"title": "Fallback Calculation", "content": '\n'.join(error_lines)}]
        })
        
        return {
            "success": True,
            "result": result,
            "fermat_applied": False,
            "reason": "Modulus is not prime",
            "sections": all_sections
        }
    
    # Section 3: Divisibility Check
    div_lines = []
    div_lines.append("═" * 55)
    div_lines.append("STEP 2: DIVISIBILITY CHECK")
    div_lines.append("═" * 55)
    div_lines.append("")
    div_lines.append(f"Check if base a = {base} is divisible by p = {modulus}")
    div_lines.append("")
    div_lines.append(f"  {base} mod {modulus} = {base % modulus}")
    div_lines.append("")
    
    if base % modulus == 0:
        div_lines.append(f"Since {base} is divisible by {modulus}:")
        div_lines.append(f"  {base} ≡ 0 (mod {modulus})")
        div_lines.append(f"  Therefore: {base}^{exponent} ≡ 0 (mod {modulus})")
        div_lines.append("")
        div_lines.append(f"<b>★ {base}^{exponent} mod {modulus} = 0</b>")
        
        all_sections.append({
            "section": "Step 2: Divisibility Check",
            "subsections": [{"title": "Base divisible by modulus", "content": '\n'.join(div_lines)}]
        })
        
        return {
            "success": True,
            "result": 0,
            "fermat_applied": True,
            "sections": all_sections
        }
    
    div_lines.append(f"✓ {base} is NOT divisible by {modulus}")
    div_lines.append(f"  gcd({base}, {modulus}) = 1")
    div_lines.append("")
    div_lines.append("Fermat's Little Theorem can be applied!")
    
    all_sections.append({
        "section": "Step 2: Divisibility Check",
        "subsections": [{"title": "Coprimality verified", "content": '\n'.join(div_lines)}]
    })
    
    # Section 4: Apply Fermat's Theorem
    fermat_lines = []
    fermat_lines.append("═" * 55)
    fermat_lines.append("STEP 3: APPLY FERMAT'S LITTLE THEOREM")
    fermat_lines.append("═" * 55)
    fermat_lines.append("")
    fermat_lines.append("Theorem Statement:")
    fermat_lines.append(f"  a^(p-1) ≡ 1 (mod p)")
    fermat_lines.append(f"  {base}^({modulus}-1) ≡ 1 (mod {modulus})")
    fermat_lines.append(f"  {base}^{modulus - 1} ≡ 1 (mod {modulus})")
    fermat_lines.append("")
    fermat_lines.append("─" * 55)
    fermat_lines.append("")
    fermat_lines.append("Exponent Reduction:")
    fermat_lines.append(f"  Since a^(p-1) = 1, we can reduce by (p-1)")
    fermat_lines.append("")
    
    fermat_power = modulus - 1
    reduced_exp = exponent % fermat_power
    
    fermat_lines.append(f"  Original exponent: E = {exponent}")
    fermat_lines.append(f"  Reduction modulus: p - 1 = {modulus} - 1 = {fermat_power}")
    fermat_lines.append("")
    fermat_lines.append(f"  E_new = E mod (p-1)")
    fermat_lines.append(f"        = {exponent} mod {fermat_power}")
    fermat_lines.append(f"        = {exponent} ÷ {fermat_power} = {exponent // fermat_power} remainder {reduced_exp}")
    fermat_lines.append(f"        = {reduced_exp}")
    fermat_lines.append("")
    fermat_lines.append(f"<b>Reduced problem: {base}^{reduced_exp} mod {modulus}</b>")
    fermat_lines.append("")
    
    if exponent > 100:
        fermat_lines.append(f"(Reduced exponent from {exponent} to just {reduced_exp}!)")
    
    all_sections.append({
        "section": "Step 3: Apply Fermat's Theorem",
        "subsections": [{"title": "Exponent Reduction", "content": '\n'.join(fermat_lines)}]
    })
    
    # Section 5: Final Calculation
    calc_lines = []
    calc_lines.append("═" * 55)
    calc_lines.append("STEP 4: FINAL CALCULATION")
    calc_lines.append("═" * 55)
    calc_lines.append("")
    calc_lines.append(f"Compute: {base}^{reduced_exp} mod {modulus}")
    calc_lines.append("")
    
    # Show step-by-step if small
    if reduced_exp <= 15 and reduced_exp > 0:
        calc_lines.append("Step-by-step multiplication:")
        calc_lines.append("")
        current = 1
        for i in range(reduced_exp):
            old = current
            current = (current * base) % modulus
            calc_lines.append(f"  {base}^{i+1} mod {modulus}: {old} × {base} = {old * base} mod {modulus} = {current}")
        calc_lines.append("")
    elif reduced_exp == 0:
        calc_lines.append(f"  {base}^0 = 1 (any number to power 0 is 1)")
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
        "fermat_applied": True,
        "fermat_power": fermat_power,
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
        self.wfile.write(json.dumps({"status": "Fermat's Little Theorem API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            base = int(data.get('base', 3))
            exponent = int(data.get('exponent', 100))
            modulus = int(data.get('modulus', 7))
            
            result = fermat_theorem_detailed(base, exponent, modulus)
            
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
