from http.server import BaseHTTPRequestHandler
import json
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """Returns (gcd, x, y) such that a*x + b*y = gcd"""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(e, phi):
    """Find d such that e*d ≡ 1 (mod phi)"""
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        return None
    return x % phi

def mod_exp_detailed(base, exp, mod):
    """Modular exponentiation with detailed steps"""
    steps = []
    steps.append(f"Computing {base}^{exp} mod {mod}")
    steps.append("")
    
    if exp == 0:
        steps.append("Result: 1 (any number to power 0 is 1)")
        return 1, '\n'.join(steps)
    
    # Binary representation approach
    exp_binary = bin(exp)[2:]
    steps.append(f"Step 1: Convert exponent to binary")
    steps.append(f"  {exp} in binary = {exp_binary}")
    steps.append(f"  Number of bits = {len(exp_binary)}")
    steps.append("")
    
    # Compute powers of base^(2^i) mod n
    steps.append("Step 2: Compute powers of 2 using repeated squaring")
    powers = {}
    current = base % mod
    power_of_2 = 1
    
    for i in range(len(exp_binary)):
        powers[power_of_2] = current
        steps.append(f"  {base}^{power_of_2} mod {mod} = {current}")
        if i < len(exp_binary) - 1:
            current = (current * current) % mod
            power_of_2 *= 2
    
    steps.append("")
    steps.append("Step 3: Combine powers based on binary representation")
    steps.append(f"  {exp} = " + " + ".join([str(2**i) for i, bit in enumerate(reversed(exp_binary)) if bit == '1']))
    steps.append("")
    
    result = 1
    for i, bit in enumerate(reversed(exp_binary)):
        power_of_2 = 2**i
        if bit == '1':
            old_result = result
            result = (result * powers[power_of_2]) % mod
            steps.append(f"  Multiply by {base}^{power_of_2} mod {mod} = {powers[power_of_2]}")
            steps.append(f"    {old_result} × {powers[power_of_2]} mod {mod} = {result}")
    
    steps.append("")
    steps.append(f"Final Result: {base}^{exp} mod {mod} = {result}")
    
    return result, '\n'.join(steps)

def extended_euclidean_detailed(e, phi):
    """Extended Euclidean Algorithm with simple dividers for RSA"""
    lines = []
    
    # Header
    lines.append("═" * 55)
    lines.append("EXTENDED EUCLIDEAN ALGORITHM")
    lines.append(f"Finding d such that e × d ≡ 1 (mod φ(n))")
    lines.append(f"Where e = {e} and φ(n) = {phi}")
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
    r1, r2 = phi, e
    s1, s2 = 1, 0
    t1, t2 = 0, 1
    
    # Computation table
    lines.append("COMPUTATION TABLE:")
    lines.append("─" * 45)
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
    
    lines.append("─" * 45)
    lines.append(f"GCD({e}, {phi}) = {r1}")
    lines.append("")
    
    # Step-by-step calculations with simple dividers
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
    
    lines.append("")
    
    if r1 != 1:
        lines.append("═" * 55)
        lines.append("RESULT: NO INVERSE EXISTS")
        lines.append(f"GCD({e}, {phi}) = {r1} ≠ 1")
        lines.append("═" * 55)
        return None, '\n'.join(lines)
    
    d = t1
    if d < 0:
        lines.append("ADJUSTMENT:")
        lines.append("─" * 40)
        lines.append(f"Coefficient t = {d} is negative")
        lines.append(f"Adjusting: {d} + {phi} = {d + phi}")
        lines.append("─" * 40)
        lines.append("")
        d = d + phi
    
    lines.append("═" * 55)
    lines.append("RESULT")
    lines.append("═" * 55)
    lines.append(f"GCD({e}, {phi}) = 1 ✓")
    lines.append("")
    lines.append(f"★ Private key d = {d}")
    lines.append("")
    lines.append("Verification:")
    lines.append(f"  {e} × {d} mod {phi} = {(e * d) % phi} ✓")
    lines.append("═" * 55)
    
    return d, '\n'.join(lines)

def rsa_encrypt_detailed(p, q, e, m):
    """Full RSA with detailed steps"""
    all_sections = []
    
    # Section 1: Input Parameters
    input_content = f"""Given Parameters:
  Prime p = {p}
  Prime q = {q}
  Public exponent e = {e}
  Message m = {m}"""
    
    all_sections.append({
        "section": "Input Parameters",
        "subsections": [{"title": "Given Values", "content": input_content}]
    })
    
    # Section 2: Calculate n
    n = p * q
    n_content = f"""n = p × q
n = {p} × {q}
n = {n}

This is the modulus used for encryption and decryption."""
    
    all_sections.append({
        "section": "Calculate n (Modulus)",
        "subsections": [{"title": "Computation", "content": n_content}]
    })
    
    # Section 3: Calculate φ(n) - Euler's Totient
    phi = (p - 1) * (q - 1)
    phi_content = f"""Euler's Totient Function:
φ(n) = (p - 1) × (q - 1)
φ({n}) = ({p} - 1) × ({q} - 1)
φ({n}) = {p-1} × {q-1}
φ({n}) = {phi}

This represents the count of integers less than n that are coprime to n."""
    
    all_sections.append({
        "section": "Calculate φ(n) - Euler's Totient",
        "subsections": [{"title": "Computation", "content": phi_content}]
    })
    
    # Section 4: Verify e is valid
    gcd_val = gcd(e, phi)
    gcd_content = f"""For e to be valid, gcd(e, φ(n)) must equal 1

gcd({e}, {phi}) = {gcd_val}

{"✓ Valid: e and φ(n) are coprime" if gcd_val == 1 else "✗ Invalid: e and φ(n) are not coprime"}"""
    
    all_sections.append({
        "section": "Verify Public Exponent e",
        "subsections": [{"title": "GCD Check", "content": gcd_content}]
    })
    
    if gcd_val != 1:
        return {
            "success": False,
            "error": f"Invalid e: gcd({e}, {phi}) = {gcd_val}, must be 1"
        }
    
    # Section 5: Find d using Extended Euclidean
    d, d_steps = extended_euclidean_detailed(e, phi)
    
    all_sections.append({
        "section": "Calculate Private Key d",
        "subsections": [{"title": "Extended Euclidean Algorithm", "content": d_steps}]
    })
    
    # Section 6: Display Keys
    keys_content = f"""PUBLIC KEY:
  (e, n) = ({e}, {n})
  Used for: Encryption

PRIVATE KEY:
  (d, n) = ({d}, {n})
  Used for: Decryption"""
    
    all_sections.append({
        "section": "Key Pair Generated",
        "subsections": [{"title": "Public and Private Keys", "content": keys_content}]
    })
    
    # Section 7: Encryption
    if m >= n:
        return {
            "success": False,
            "error": f"Message m ({m}) must be less than n ({n})"
        }
    
    c, enc_steps = mod_exp_detailed(m, e, n)
    enc_content = f"""Encryption Formula: c = m^e mod n
c = {m}^{e} mod {n}

{enc_steps}

Ciphertext c = {c}"""
    
    all_sections.append({
        "section": "Encryption Process",
        "subsections": [{"title": "Modular Exponentiation", "content": enc_content}]
    })
    
    # Section 8: Decryption
    m_dec, dec_steps = mod_exp_detailed(c, d, n)
    dec_content = f"""Decryption Formula: m = c^d mod n
m = {c}^{d} mod {n}

{dec_steps}

Decrypted Message m = {m_dec}"""
    
    all_sections.append({
        "section": "Decryption Process",
        "subsections": [{"title": "Modular Exponentiation", "content": dec_content}]
    })
    
    # Section 9: Final Result
    result_content = f"""RSA COMPLETE

Original Message:    m = {m}
Encrypted Ciphertext: c = {c}
Decrypted Message:   m = {m_dec}

Public Key:  (e, n) = ({e}, {n})
Private Key: (d, n) = ({d}, {n})

{"✓ Verification: Original message matches decrypted message!" if m == m_dec else "✗ Error: Messages don't match!"}"""
    
    all_sections.append({
        "section": "Final Result",
        "subsections": [{"title": "Summary", "content": result_content}]
    })
    
    return {
        "success": True,
        "p": p,
        "q": q,
        "n": n,
        "phi": phi,
        "e": e,
        "d": d,
        "m": m,
        "c": c,
        "m_decrypted": m_dec,
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
        self.wfile.write(json.dumps({"status": "RSA API ready"}).encode('utf-8'))
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            p = data.get('p', 17)
            q = data.get('q', 13)
            e = data.get('e', 3)
            m = data.get('m', 9)
            
            result = rsa_encrypt_detailed(p, q, e, m)
            
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